from app import db
from app.db_models import MovieItem

def get_user_movies(user_id: int) -> list:
    return MovieItem.query.filter_by(user_id=user_id).all()