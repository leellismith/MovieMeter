import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
        api_url = os.environ.get("OMDBAPI_HOST")
        api_url += "apikey="
        api_url += os.environ.get("OMDBAPI_KEY")
        api_url += "&t="
        api_url += query
        response = requests.get(api_url)
        if response.status_code == 200:
            if 'Error' not in [response.json()]:
                movie_data = response.json()
                movies = {
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
                mongo.db.movies.insert_one(movies)
    return render_template("index.html", movies=movies)
    


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
