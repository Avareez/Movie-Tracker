from flask import Blueprint, render_template, request
from app.services.tmdb import search_movies

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