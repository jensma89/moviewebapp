"""
fetch_movie.py
"""
import requests
import os



API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_date(title):
    """Fetch movie data from omdb API"""
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data.get("Title"),
            "director": data.get("Director"),
            "year": data.get("Year"),
            "poster_url": data.get("Poster"),
        }
    return None
