from flask import (Flask, redirect, render_template,
                   request, url_for)
from data_manager import DataManager
from models import db, Movie
from dotenv import load_dotenv
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





load_dotenv()
api_key = os.getenv("OMDB_API_KEY")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)