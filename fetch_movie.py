"""
fetch_movie.py

Fetch the movie data from OMDb API.
"""
import requests
import os

API_KEY = os.getenv("OMDB_API_KEY")

def fetch_movie_data(title):
    """Fetch movie data from OMDb API"""
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise HTTP error as exception
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie '{title}': {e}")
        return None

    try:
        data = response.json()
    except ValueError as e:
        print(f"Error decoding JSON for movie '{title}': {e}")
        return None

    # Check for existing data
    if not data.get("Title"):
        print(f"Movie '{title}' not found in OMDb API.")
        return None

    return {
        "title": data.get("Title"),
        "director": data.get("Director"),
        "year": data.get("Year"),
        "poster_url": data.get("Poster"),
    }
