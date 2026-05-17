from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.services.tmdb import search_movies, get_movie_details
from app.services.movies import get_user_movies_service, add_user_movie_service, delete_user_movie_service, update_user_movie_service

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    movies = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            movies = search_movies(query)
    return render_template("index.html", movies=movies, query=query)

@main_bp.route("/movie/<int:tmdb_id>")
def movie_details(tmdb_id):
    movie = get_movie_details(tmdb_id)
    error = request.args.get("error")
    return render_template("movie_details.html", movie=movie, error=error)

@main_bp.route("/users/<int:user_id>/movies")
def user_movies(user_id):
    movies = get_user_movies_service(user_id)
    is_owner = current_user.is_authenticated and current_user.id == user_id

    detailed_movies = []
    for movie in movies:
        details = get_movie_details(movie.tmdb_id)
        detailed_movies.append({
            "id": movie.id,
            "tmdb_id": movie.tmdb_id,
            "status": movie.status,
            "user_rating": movie.user_rating,
            "title": details.get("title", "Unknown Title") if details else "Unknown Title",
            "poster_url": details.get("poster_url") if details else None,
        })

    return render_template("user_movies.html", movies=detailed_movies, is_owner=is_owner, user_id=user_id)

@main_bp.route("/movie/<int:tmdb_id>/add", methods=["POST"])
@login_required
def add_movie(tmdb_id):
    movie, error = add_user_movie_service(current_user.id, tmdb_id)
    if error:
        return redirect(url_for("main.movie_details", tmdb_id=tmdb_id, error=error))
    return redirect(url_for("main.user_movies", user_id=current_user.id))

@main_bp.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
@login_required
def delete_movie(user_id, movie_id):
    if current_user.id != user_id:
        return redirect(url_for("main.user_movies", user_id=user_id))
    delete_user_movie_service(user_id, movie_id)
    return redirect(url_for("main.user_movies", user_id=current_user.id))

@main_bp.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
@login_required
def update_movie(user_id, movie_id):
    if current_user.id != user_id:
        return redirect(url_for("main.user_movies", user_id=user_id))
    
    status = request.form.get("status")
    user_rating = request.form.get("user_rating", type=float)
    update_user_movie_service(user_id, movie_id, status=status, user_rating=user_rating)
    return redirect(url_for("main.user_movies", user_id=current_user.id))