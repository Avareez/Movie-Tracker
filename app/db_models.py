from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship("MovieItem", backref="owner", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class MovieItem(db.Model):
    __tablename__ = "movie_items"
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Plan to watch")
    user_rating = db.Column(db.Float, nullable=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<MovieItem tmdb={self.tmdb_id}>"