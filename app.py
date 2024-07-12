import os
import requests
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, jsonify, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

# Initialize Flask
app = Flask(__name__)

# Configuration
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Initialize PyMongo
mongo = PyMongo(app)

# Routes
@app.route("/")
@app.route("/index")
def index():
    movies = mongo.db.movies.find()
    return render_template("index.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    if not query:
        flash(f"No search provided.")
        return render_template("index.html")

    redirect_to = request.form.get("redirect_to", "index")
    movies = search_movies_in_db(query)

    if not movies:
        movies = search_movies_in_api(query)
        if movies:
            save_movies_to_db(movies)
    
    if not movies:
        if redirect_to == "add_review":
            flash(f"No movies found for '{query}'.")
            return render_template("add_review.html", movie_title=query)
        return render_template("index.html", error=f"No movies found for '{query}'.")
        
    if redirect_to == "add_review":
        poster_url = movies[0].get("Poster") if movies else None
        return render_template(
            "add_review.html", movie_title=query, poster_url=poster_url)
    
    return render_template("index.html", movies=movies)


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    movies = search_movies(query)    
    return jsonify([movie["Title"] for movie in movies])
    

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # checks mongodb to see if username exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Checks database to see if user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user and check_password_hash(existing_user["password"], request.form.get("password")):
            session["user"] = request.form.get("username").lower()
            flash(f"Welcome, {request.form.get('username')}")
            return redirect(url_for("profile", username=session["user"]))
        flash("Incorrect Username and/or Password")
    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    if "user" in session:
        user = mongo.db.users.find_one({"username": session["user"]})
        if user and user["username"] == username:
            return render_template("profile.html", username=username)
        flash("You are only able to view your own profile!")
        return redirect(url_for("profile", username=session["user"]))
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    movie_title = ""
    review_text = ""
    poster_url = ""

    if request.method == "POST":
        movie_title = request.form.get("query")
        review_text = request.form.get("review")
        poster_url = request.form.get("poster_url")

        if not movie_title or not review_text:
            flash("Movie title and review text are required.")
            return render_template(
                "add_review.html", movie_title=movie_title, 
                review_text=review_text, poster_url=poster_url)

        if len(review_text) > 200:
            flash("A review must be 200 characters or less.")
            return render_template(
                "add_review.html", movie_title=movie_title, 
                review_text=review_text, poster_url=poster_url)

        movie_details = get_movie_details(movie_title)

        if not movie_details:
            movie_details = search_movies_in_api(movie_title)
            if movie_details:
                save_movies_to_db(movie_details)

        if not movie_details:
            flash(f"Movie '{movie_title}' not found.")
            return render_template(
                "add_review.html", movie_title=movie_title, 
                review_text=review_text, poster_url=poster_url)

        review = {
            "movie": movie_title,
            "review": review_text,
            "image_url": poster_url,
            "user": session.get("user"),
            "timestamp": datetime.datetime.utcnow()
        }

        mongo.db.reviews.insert_one(review)
        flash("Review added successfully.")
        return redirect(url_for("reviews"))

    return render_template(
        "add_review.html", movie_title=movie_title,
        review_text=review_text, poster_url=poster_url)


@app.route("/reviews")
def reviews():
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


@app.route("/manage_reviews", methods=["GET"])
def manage_reviews():
    user = session.get("user")
    reviews = list(mongo.db.reviews.find({"user": user}))
    return render_template("manage_reviews.html", reviews=reviews)


@app.route("/manage_reviews/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    if request.method == "POST":
        edit_review = request.form.get("review")

        if not edit_review:
            flash("A review field can't be empty.")
            return render_template("manage_reviews.html", review=review)

        if len(edit_review) > 200:
            flash("A review must be 200 characters or less.")
            return render_template("manage_reviews.html", review=review)

        mongo.db.reviews.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": {"review": edit_review, "timestamp": datetime.datetime.utcnow()}}
        )
        flash("You have updated your review.")
        return redirect(url_for("manage_reviews"))

    return render_template("manage_reviews.html",  reviews=[], review=review)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash("Your review has been deleted!")
    return redirect(url_for("manage_reviews"))



# Help Functions
def search_movies(query):
    movies = search_movies_in_db(query)
    if not movies:
        movies = search_movies_in_api(query)
        if movies:
            save_movies_to_db(movies)
    return movies


def search_movies_in_db(query):
    return list(mongo.db.movies.find({"$text": {"$search": query}}))


def search_movies_in_api(query):
    api_url = os.environ.get(
        "OMDBAPI_HOST") + "apikey=" + os.environ.get(
            "OMDBAPI_KEY") + "&s=" + query + "&type=movie"
    response = requests.get(api_url)
    if response.status_code == 200:
        search_results = response.json()
        if 'Search' in search_results:
            movies = []
            for movie in search_results['Search']:
                movie_details = get_movie_details(movie['imdbID'])
                if movie_details:
                    movies.append(movie_details)
            return movies
    return None


def get_movie_details(imdb_id):
    api_url = os.environ.get(
        "OMDBAPI_HOST") + "apikey=" + os.environ.get(
            "OMDBAPI_KEY") + "&i=" + imdb_id
    response = requests.get(api_url)
    if response.status_code == 200:
        movie_data = response.json()
        if 'Error' not in movie_data:
            return {
                "Title": movie_data.get("Title"),
                "Actors": movie_data.get("Actors"),
                "Director": movie_data.get("Director"),
                "Genre": movie_data.get("Genre"),
                "Poster": movie_data.get("Poster"),
                "Rated": movie_data.get("Rated"),
                "Released": movie_data.get("Released"),
                "Runtime": movie_data.get("Runtime"),
                "Year": movie_data.get("Year"),
                "imdbID": movie_data.get("imdbID")
            }
    return None


def save_movies_to_db(movies):
    for movie in movies:
        if not mongo.db.movies.find_one({"imdbID": movie.get("imdbID")}):
            mongo.db.movies.insert_one(movie)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
