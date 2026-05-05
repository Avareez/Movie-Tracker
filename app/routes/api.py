from flask import Blueprint, jsonify
from app.services.movies import get_user_movies

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    movies = get_user_movies(user_id)
    return jsonify([{
        "id": m.id,
        "tmdb_id": m.tmdb_id,
        "status": m.status,
        "user_rating": m.user_rating,
        "added_date": m.added_date.isoformat()
    } for m in movies]), 200