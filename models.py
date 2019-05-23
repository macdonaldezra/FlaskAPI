from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # must be initialized using create_app

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    password = db.Column(db.String(128))

    def __repr__(self):
        return ('<User {} {}>'.format(self.first_name, self.last_name))
    
    def add(self):
        self.hash_password()
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def hash_password(self):
        hasher = PasswordHasher()
        self.password = hasher.hash(self.password)

    def verify_password(self, password):
        try:
            hasher = PasswordHasher()
            hasher.verify(self.password, password)
            return True
        except VerifyMismatchError: # perhaps add messages later
            return False
        except InvalidHash:
            return False
