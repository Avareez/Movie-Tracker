from app import db
from app.db_models import MovieItem

def get_user_movies_service(user_id: int) -> list:
    return MovieItem.query.filter_by(user_id=user_id).all()

def add_user_movie_service(user_id: int, tmdb_id: int, status: str = "Plan to Watch") -> tuple[MovieItem, str]:
    existing_movie = MovieItem.query.filter_by(user_id=user_id, tmdb_id=tmdb_id).first()
    if existing_movie:
        return None, "Movie already on your list"
    
    movie = MovieItem(user_id=user_id, tmdb_id=tmdb_id, status=status)
    db.session.add(movie)
    db.session.commit()
    return movie, None

def delete_user_movie_service(user_id: int, movie_id: int) -> tuple[bool, str]:
    movie = MovieItem.query.filter_by(id=movie_id, user_id=user_id).first()
    if not movie:
        return False, "Movie not found"
    db.session.delete(movie)
    db.session.commit()
    return True, None

def update_user_movie_service(user_id: int, movie_id: int, status: str = None, user_rating: float = None) -> tuple[MovieItem, str]:
    movie = MovieItem.query.filter_by(id=movie_id, user_id=user_id).first()
    if not movie:
        return None, "Movie not found"
    if status:
        movie.status = status
    if user_rating is not None:
        movie.user_rating = user_rating
    db.session.commit()
    return movie, None