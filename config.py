import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#Path to keys.env file 
load_dotenv(os.path.join(BASE_DIR, "keys.env"))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY")

    API_KEY = os.getenv("TMDB_API_KEY")

