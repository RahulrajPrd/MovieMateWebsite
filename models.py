# models.py
import pickle

# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


with open('E:\lang\MOVIE-RECOMMODATION-SYSTEM\MOVIES\Movies\model\movies.pkl', 'rb') as file:
    m = pickle.load(file)

with open("E:/lang/MOVIE-RECOMMODATION-SYSTEM/MOVIES/Movies/model/similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

titles = m['title']
