from flask import (Flask, redirect, render_template,
                   request, url_for)
from data_manager import DataManager
from models import db, Movie
from dotenv import load_dotenv
from fetch_movie import fetch_movie_data
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///"
                                         f"{os.path.join(
                                             basedir, 
                                             'data/movies.db')}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Link database to app

data_manager = DataManager() # Create a object from DataManager class


@app.get("/")
def home():
    """Load and show the home page template
    and a list of all users, with add new user form."""
    users = data_manager.get_users()
    return render_template("index.html",
                           users=users)


@app.post("/users")
def submit_new_user_to_database():
    """If the form add user is submitted,
    create a new user in db and redirect to home."""
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for("home"))


@app.get("/users/<int:user_id>/movies")
def list_user_movies(user_id):
    """Show all favorite movies for a specific user."""
    user = data_manager.get_user_by_id(user_id)
    movies = user.movies
    return render_template("user_movies.html",
                           user=user,
                           movies=movies)


@app.post("/users/<int:user_id>/movies")
def add_movie_to_list(user_id):
    """Add a movie to the database of a specific user."""
    title = request.form.get("title")

    if not title:
        return redirect(url_for(
            "list_user_movies",
            user_id=user_id))

    # OMDb request
    movie_data = fetch_movie_data(title)

    if not movie_data: # Movie not found
        return redirect(url_for(
            "list_user_movies",
            user_id=user_id))

    # Set user ID
    movie_data['user_id'] = user_id

    # Save movie to database
    data_manager.add_movie(movie_data)
    return redirect(url_for(
        "list_user_movies",
        user_id=user_id))



@app.post("/users/<int:user_id>/movies/<int:movie_id>/update")
def update_movie_title(user_id, movie_id):
    """Change the movie title without OMDb correction"""
    new_title = request.form.get("title")
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for(
        "list_user_movies",
        user_id=user_id))


@app.post("/users/<int:user_id>/movies/<int:movie_id>/delete")
def delete_movie(user_id, movie_id):
    """Delete a movie from the database of a specific user."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for(
        "list_user_movies",
        user_id=user_id))



@app.errorhandler(400)
def bad_request(error):
    return render_template("400.html"), 400


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500



# Secret API key
load_dotenv()
api_key = os.getenv("OMDB_API_KEY")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)