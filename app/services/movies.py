from app import db
from app.db_models import MovieItem

def get_user_movies(user_id: int) -> list:
    return MovieItem.query.filter_by(user_id=user_id).all()

def add_movie_to_user(user_id: int, tmdb_id: int, status: str = "Plan to Watch") -> tuple[MovieItem, str]:
    existing_movie = MovieItem.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
    if existing_movie:
        return None, "Movie already on your list"
    
    movie = MovieItem(user_id=user_id, tmdb_id=tmdb_id, status=status)
    db.session.add(movie)
    db.session.commit()
    return movie, None