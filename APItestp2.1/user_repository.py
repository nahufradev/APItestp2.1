from database import db
from models import User

class UserRepository:
    def create_user(self, username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()
