from app import db
from app.db_models import User

def register_user(username: str, password: str) -> tuple[User, str]:
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None, "Username already taken"
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None

def authenticate_user(username: str, password: str) -> tuple[User, str]:
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return None, "Invalid username or password"
    return user, None