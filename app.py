import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))

    if not movies:
        api_url = os.environ.get("OMDBAPI_HOST") + "apikey=" + os.environ.get("OMDBAPI_KEY") + "&t=" + query
        print(f"API URL: {api_url}")
        response = requests.get(api_url)

        if response.status_code == 200:
            movie_data = response.json()

            if 'Error' not in movie_data:
                check_movie = mongo.db.movies.find_one({"Title": movie_data.get("Title")})
                
                if not check_movie:
                    movie_details = {
                        "Title": movie_data.get("Title"),
                        "Actors": movie_data.get("Actors"),
                        "Director": movie_data.get("Director"),
                        "Genre": movie_data.get("Genre"),
                        "Poster": movie_data.get("Poster"),
                        "Rated": movie_data.get("Rated"),
                        "Released": movie_data.get("Released"),
                        "Runtime": movie_data.get("Runtime"),
                        "Year": movie_data.get("Year")
                    }
                    mongo.db.movies.insert_one(movie_details)
                    movies = [movie_details]
                else:
                    movies = [check_movie]

    return render_template("index.html", movies=movies)
    

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
                    flash("Welcome, {}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
