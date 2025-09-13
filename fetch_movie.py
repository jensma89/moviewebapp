"""
fetch_movie.py
"""
import requests


def fetch_movie_date(title):
    api_key = "ADD MY KEY HERE"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
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
