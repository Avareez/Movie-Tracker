from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.services.tmdb import search_movies, get_movie_details
from app.services.movies import get_user_movies

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
    return render_template("movie_details.html", movie=movie)

@main_bp.route("/users/<int:user_id>/movies")
def user_movies(user_id):
    movies = get_user_movies(user_id)
    is_owner = current_user.is_authenticated and current_user.id == user_id
    return render_template("user_movies.html", movies=movies, is_owner=is_owner)