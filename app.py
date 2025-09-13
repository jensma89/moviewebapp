from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

api_key = os.getenv("OMDB_API_KEY")