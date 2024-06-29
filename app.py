import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, jsonify, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    movies = mongo.db.movies.find()
    return render_template("index.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = search_movies_in_db(query)
    
    if not movies:
        movies = search_movies_in_api(query)
        if movies:
            save_movies_to_db(movies)
        else:
            return render_template("index.html", error="No movies found.")
    
    return render_template("index.html", movies=movies)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    movies = search_movies_in_db(query)
    
    if not movies:
        movies = search_movies_in_api(query)
        if movies:
            save_movies_to_db(movies)
    
    return jsonify([movie["Title"] for movie in movies])

def search_movies_in_db(query):
    return list(mongo.db.movies.find({"$text": {"$search": query}}))

def search_movies_in_api(query):
    api_url = os.environ.get("OMDBAPI_HOST") + "apikey=" + os.environ.get("OMDBAPI_KEY") + "&s=" + query
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
    api_url = os.environ.get("OMDBAPI_HOST") + "apikey=" + os.environ.get("OMDBAPI_KEY") + "&i=" + imdb_id
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

        if existing_user:
            # ensures password matches
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(
                        url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Get the session user from session
    sess_user = session.get("user")

    if sess_user:
        # Get the session user from DB
        user = mongo.db.users.find_one({"username": sess_user})
        
        if user:
            # Check if the session user matches the username in the URL
            if user["username"] == username:
                return render_template("profile.html", username=user["username"])
            else:
                flash("You are only able to view your own profile!")
                return redirect(url_for("profile", username=user["username"]))
        else:
            flash("Can't find user in the database.")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
