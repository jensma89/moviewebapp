from flask import Flask
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
    return "Welcome to MovieWebApp"





load_dotenv()
api_key = os.getenv("OMDB_API_KEY")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)