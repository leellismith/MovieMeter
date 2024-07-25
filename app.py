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

# Create text index on 'Title' field in 'movies' collection
mongo.db.movies.create_index([("Title", "text")])


# Routes
@app.route("/")
@app.route("/index")
def index():
    """
    Renders the index page with a sample of movies
    that have valid Poster, Rated, Released, and imdbRating fields.
    """
    pipeline = [
        {
            "$match": {
                "Poster": {
                    "$exists": True,
                    "$nin": ["", "N/A"]
                },
                "Rated": {
                    "$exists": True,
                    "$nin": ["", "N/A", "Not Rated", "TV-MA"]
                },
                "Released": {
                    "$exists": True,
                    "$nin": ["", "N/A"]
                },
                "imdbRating": {
                    "$exists": True,
                    "$nin": ["", "N/A"]
                }
            }
        },
        {
            "$sample": {"size": 8}
        }
    ]

    movies = list(mongo.db.movies.aggregate(pipeline))
    return render_template("index.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Searches for movies based on user query.
    If movies are not found in the local database,
    searches the external API and saves results to the database.
    """
    query = request.form.get("query")
    if not query:
        flash(f"No search provided.")
        return render_template("index.html")

    redirect_to = request.form.get("redirect_to", "index")
    movies = search_movies(query, exact_match=True)

    if not movies:
        movies = search_movies_in_api(query)
        if movies:
            save_movies_to_db(movies)

    if not movies:
        if redirect_to == "add_review":
            flash(f"No movies found for '{query}'.")
            return render_template("add_review.html", movie_title=query)
        return render_template(
            "index.html", error=f"No movies found for '{query}'.")

    if redirect_to == "add_review":
        poster_url = movies[0].get("Poster") if movies else None
        return render_template(
            "add_review.html", movie_title=query, poster_url=poster_url)

    return render_template("index.html", movies=movies)


@app.route("/autocomplete")
def autocomplete():
    """
    Provides autocomplete suggestions for movie titles based on user query.
    """
    query = request.args.get("query")
    movies = search_movies(query, exact_match=False)
    return jsonify([movie["Title"] for movie in movies])


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles user registration.
    """
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
    """
    Handles user login.
    """
    if request.method == "POST":
        # Checks database to see if user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user and check_password_hash(
                existing_user["password"], request.form.get("password")):
            session["user"] = request.form.get("username").lower()
            flash(f"Welcome, {request.form.get('username')}")
            return redirect(url_for("profile", username=session["user"]))
        flash("Incorrect Username and/or Password")
    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    """
    Displays the user's profile page if logged in.
    """
    if "user" in session:
        user = mongo.db.users.find_one({"username": session["user"]})
        if user and user["username"] == username:
            return render_template("profile.html", username=username)
        flash("You are only able to view your own profile!")
        return redirect(url_for("profile", username=session["user"]))
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Logs the user out and redirects to the login page.
    """
    flash("You have been logged out")
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """
    Handles adding new movie reviews.
    """
    movie_title = ""
    review_text = ""
    poster_url = ""

    # Handle GET request
    if request.method == "GET":
        movie_title = request.args.get("movieTitle", "")
        poster_url = request.args.get("posterUrl", "")

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

        movie_details = search_movies_in_api(movie_title)
        if not movie_details:
            movie_details = search_movies_in_api(movie_title)
            if movie_details:
                save_movies_to_db(movie_details)

        if not movie_details:
            flash(f"Movie '{movie_title}' not found.")
            return render_template(
                "add_review.html", movie_title=movie_title,
                review_text=review_text, poster_url=poster_url)

        # Saves review to the database
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
    """
    Handles displaying all movie reviews
    """
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


@app.route("/manage_reviews", methods=["GET"])
def manage_reviews():
    """
    Displays reviews for the logged-in user to manage.
    """
    user = session.get("user")
    reviews = list(mongo.db.reviews.find({"user": user}))
    return render_template("manage_reviews.html", reviews=reviews)


@app.route("/manage_reviews/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """
    Handles the editing of an existing review.
    """
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
            {"$set": {
                "review": edit_review, "timestamp":
                    datetime.datetime.utcnow()}}
        )
        flash("You have updated your review.")
        return redirect(url_for("manage_reviews"))

    return render_template("manage_reviews.html",  reviews=[], review=review)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    """
    Deletes a review by its ID.
    """
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash("Your review has been deleted!")
    return redirect(url_for("manage_reviews"))


# Help Functions
def search_movies(query, exact_match=False):
    """
    Searches for movies in the local database and, if not found,
    searches the external API and saves results to the database.
    """
    if exact_match:
        movies = search_movies_in_db(query)
    else:
        movies = search_movies_in_api(query)
    if movies:
        save_movies_to_db(movies)
    return movies


def search_movies_in_db(query):
    """
    Searches for movies in the local database by exact match or text search.
    """
    exact_match = mongo.db.movies.find_one({"Title": query})
    if exact_match:
        return [exact_match]
    # Fallback to text search
    return list(mongo.db.movies.find({"$text": {"$search": query}}))


def search_movies_in_api(query):
    """
    Searches for movies using the external OMDB API.
    """
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
    """
    Retrieves detailed information about a movie by its IMDB ID using the OMDB API.
    """
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
                "imdbID": movie_data.get("imdbID"),
                "imdbRating": movie_data.get("imdbRating")
            }
    return None


def save_movies_to_db(movies):
    """
    Saves movie information to the local database if it doesn't already exist.
    """
    for movie in movies:
        if not mongo.db.movies.find_one({"imdbID": movie.get("imdbID")}):
            mongo.db.movies.insert_one(movie)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False
    )
