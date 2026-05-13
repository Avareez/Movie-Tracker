from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.auth import register_user, authenticate_user
from app.services.movies import get_user_movies_service, add_user_movie_service, delete_user_movie_service, update_user_movie_service

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/register", methods=["POST"])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user, error = register_user(username, password)
    if error:
        return jsonify({"error": error}), 409
    return jsonify({"message": "User created successfully"}), 201

@api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user, error = authenticate_user(username, password)
    if error:
        return jsonify({"error": error}), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 200


@api_bp.route("/users/<int:user_id>/movies", methods=["GET"])
def api_get_movies(user_id):
    movies = get_user_movies_service(user_id)
    return jsonify([{
        "id": m.id,
        "tmdb_id": m.tmdb_id,
        "status": m.status,
        "user_rating": m.user_rating,
        "added_date": m.added_date.isoformat()
    } for m in movies]), 200

@api_bp.route("/users/<int:user_id>/movies", methods=["POST"])
@jwt_required()
def api_add_movie(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
    
    tmdb_id = data.get("tmdb_id")
    if not tmdb_id:
        return jsonify({"error": "Missing TMDB ID"}), 400
    
    movie, error = add_user_movie_service(user_id, tmdb_id, data.get("status", "Plan to Watch"))
    if error:
        return jsonify({"error": error}), 409
    
    return jsonify({
        "id": movie.id,
        "tmdb_id": movie.tmdb_id,
        "status": movie.status,
        "user_rating": movie.user_rating,
        "added_date": movie.added_date.isoformat()
    }), 201

@api_bp.route("/users/<int:user_id>/movies/<int:movie_id>", methods=["DELETE"])
@jwt_required()
def api_delete_movie(user_id, movie_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    success, error = delete_user_movie_service(user_id, movie_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Movie deleted"}), 200


@api_bp.route("/users/<int:user_id>/movies/<int:movie_id>", methods=["PATCH"])
@jwt_required()
def api_update_movie(user_id, movie_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    movie, error = update_user_movie_service(
        user_id, movie_id,
        status=data.get("status"),
        user_rating=data.get("user_rating")
    )
    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "id": movie.id,
        "tmdb_id": movie.tmdb_id,
        "status": movie.status,
        "user_rating": movie.user_rating,
        "added_date": movie.added_date.isoformat()
    }), 200