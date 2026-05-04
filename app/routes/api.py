from flask import Blueprint, jsonify, request
from app import db
from app.db_models import MovieItem

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    movies = MovieItem.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": m.id,
        "tmdb_id": m.tmdb_id,
        "status": m.status,
        "user_rating": m.user_rating,
        "added_date": m.added_date.isoformat()
    } for m in movies]), 200