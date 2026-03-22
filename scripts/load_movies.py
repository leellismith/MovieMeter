import requests
from pymongo import MongoClient
import time

TMDB_API_KEY = "913f71da7677dccc656d5989fb00994e"
OMDB_API_KEY = "eec72b53"

# --- CONNECT TO MONGODB ATLAS ---
client = MongoClient(
    "mongodb+srv://leellismith:k6teBvpP37tU3p7k@myfirstcluster.5oybg2o.mongodb.net/moviemeter?retryWrites=true&w=majority&appName=myFirstCluster"
)

db = client["moviemeter"]
collection = db["movies"]


def fetch_tmdb_top_rated(page):
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US&page={page}"
    response = requests.get(url)
    return response.json().get("results", [])


def fetch_omdb_details(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
    response = requests.get(url)
    return response.json()


def movie_is_valid(movie):
    # Reject missing posters or missing IMDb ratings
    if movie.get("Poster") in ["N/A", None]:
        return False
    if movie.get("imdbRating") in ["N/A", None]:
        return False
    try:
        return float(movie["imdbRating"]) >= 7.0
    except:
        return False


def save_movie(movie):
    imdb_id = movie.get("imdbID")
    if not imdb_id:
        return

    # Avoid duplicates
    if collection.find_one({"imdbID": imdb_id}):
        return

    collection.insert_one(movie)
    print(f"Saved: {movie.get('Title')} ({movie.get('Year')})")


def main():
    target_count = 500
    saved_count = collection.count_documents({})
    page = 1

    print(f"Starting with {saved_count} movies in the database.")

    while saved_count < target_count:
        print(f"\nFetching TMDB page {page}...")
        tmdb_movies = fetch_tmdb_top_rated(page)

        if not tmdb_movies:
            print("No more TMDB results. Stopping.")
            break

        for tmdb_movie in tmdb_movies:
            imdb_id = tmdb_movie.get("imdb_id")

            # If TMDB didn't include IMDb ID, fetch details
            if not imdb_id:
                details_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie['id']}?api_key={TMDB_API_KEY}"
                details = requests.get(details_url).json()
                imdb_id = details.get("imdb_id")

            if not imdb_id:
                continue

            omdb_movie = fetch_omdb_details(imdb_id)

            if movie_is_valid(omdb_movie):
                save_movie(omdb_movie)
                saved_count += 1

                if saved_count >= target_count:
                    break

            time.sleep(0.25)  # gentle rate limiting

        page += 1

    print(f"\nDone! You now have {saved_count} movies in your database.")


if __name__ == "__main__":
    main()