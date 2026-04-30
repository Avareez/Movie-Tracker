import requests
from flask import current_app

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def search_movies(query: str) -> list:
    url = f"{TMDB_BASE_URL}/search/movie"
    headers = {
        "Authorization": f"Bearer {current_app.config['TMDB_API_KEY']}"
    }
    params = {
        "query": query,
        "language": "en-US",
    }

    response = requests.get(url, headers=headers, params=params, timeout=5)
    response.raise_for_status()

    movies = response.json().get("results", [])
    for movie in movies:
        poster = movie.get("poster_path")
        movie["poster_url"] = f"{TMDB_IMAGE_BASE_URL}{poster}" if poster else None

    return movies

def get_movie_details(tmdb_id: int) -> dict | None:
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    headers = {
        "Authorization": f"Bearer {current_app.config['TMDB_API_KEY']}"
    }
    params = {
        "language": "en-US",
    }

    response = requests.get(url, headers=headers, params=params, timeout=5)
    response.raise_for_status()

    movie = response.json()
    poster = movie.get("poster_path")
    movie["poster_url"] = f"{TMDB_IMAGE_BASE_URL}{poster}" if poster else None

    return movie