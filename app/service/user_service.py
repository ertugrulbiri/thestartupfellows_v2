from app import db
from app.model.user_models import User


def login_service(username, password, keyword):
    user = db.session.query(User).filter(User.email == username).first()
    if user is None:
        return None
    elif user.check_password(password):
        return user