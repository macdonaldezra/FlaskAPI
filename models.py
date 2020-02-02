# -*- coding: utf-8 -*-
"""Models and required database functionality for User, Client, and Project.

Classes are designed to encapsulate as much database writing functionality as possible,
hence, data is expected to be sufficiently clean before functions in this module are
called. In a perfect world, this encourages more readable and condensed view method code.
"""

import jwt

from datetime import datetime, timedelta
from flask import current_app
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from flask_sqlalchemy import SQLAlchemy, BaseQuery

db = SQLAlchemy()


class QueryWithSoftDelete(BaseQuery):
    # Class implements soft delete feature taken from Miguel Grinberg tutorial.
      # https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy
      # This class is used in the User class to provide a means of making users 
      # non-searchable when deleted is set to true.
      # At this point the API does not use this soft delete feature when deleting users.
    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)


class User(db.Model):
    """User contains information about a given user and includes CRUD functionality for each user.

    Features:
    * User's are identified by a unique username
    * User can be deleted permanently from database or simply removed from database returned searches
        using soft-delete.
    """

    __tablename__ = 'user'
    query_class = QueryWithSoftDelete

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    password = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean(), default=False)
    deleted_on = db.Column(db.DateTime, default=datetime.utcnow)
    clients = db.relationship('Client', backref='user', lazy='dynamic')

    def __repr__(self) -> str:
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

    def check_deleted(self) -> bool:
        return self.deleted

    def delete(self):
        # Save delete date and remove entry from database query
        if self.deleted is False:
            self.deleted = True
            self.deleted_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def permanently_delete(self):
        # permanently delete a user from the database.
        db.session.delete(self)
        db.session.commit()

    def hash_password(self):
        hasher = PasswordHasher()
        self.password = hasher.hash(self.password)

    def verify_password(self, password: str) -> bool:
        # Return false if passwords do not match or if 
          # password hash has been tampered.
        try:
            hasher = PasswordHasher()
            hasher.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False
        except InvalidHash:
            return False

    def generate_username_token(self, days: int = 1, seconds: int = 60):
        # Generate a new token based on provided username
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=days, seconds=seconds),
                'iat': datetime.utcnow(),
                'username': self.username
            }
            return jwt.encode(
                payload,
                current_app.config['PRIVATE_KEY'].encode('utf-8'),
                algorithm='RS256'
            ).decode('utf-8')
        except:
            return False

    def confirm_user(self, token: str) -> bool:
        # Create user and return true if provided token is valid, otherwise return false
        try:
            data = jwt.decode(token, current_app.config['PUBLIC_KEY'].encode('utf-8'),
                algorithms=['RS256'])
            if data['username'] != self.username:
                return False
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def generate_email_change_token(self, new_email: str, days: int = 1, seconds: int = 60):
        # Generate new token for user to validate new email address
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=days, seconds=seconds),
                'iat': datetime.utcnow(),
                'username': self.username,
                'new_email': new_email
            }
            return jwt.encode(
                payload,
                current_app.config['PRIVATE_KEY'].encode('utf-8'),
                algorithm='RS256'
            ).decode('utf-8')
        except:
            return False

    def confirm_email_change(self, token: str) -> bool:
        # Verify that token associated with new e-mail matches, otherwise return false
        try:
            data = jwt.decode(token, current_app.config['PUBLIC_KEY'].encode('utf-8'),
                algorithms=['RS256'])
            if data['username'] != self.username:
                return False
            if data['new_email'] is None:
                return False
            self.email = data['new_email']
            db.session.add(self)
            db.session.commit()
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def get_client(self, name: str, email: str):
        # Retrieve a client based on provided user (self), and the
          # client's name and email.
        return self.clients.filter_by(name=name, email=email).first()

    def get_clients(self) -> list:
        return self.clients.all()


class Client(db.Model):
    """Clients are created and managed by a User.
    
    * A client can be deleted using soft-delete or permanent delete.
    """
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(150))
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    projects = db.relationship('Project', backref='client', lazy='dynamic')
    deleted = db.Column(db.Boolean(), default=False)
    deleted_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def add(self, user, **kwargs):
        self.users = user
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        if self.deleted is False:
            self.deleted = True
            self.deleted_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def permanently_delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return ('<Client {}>'.format(self.name))

class Project(db.Model):
    """Projects are created and managed by a User, with respect to a Client.
    
    * A project can be deleted using soft-delete or permanent delete.
    """

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), unique=True)
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Boolean(), default=False)
    deleted_on = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, user_id, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        if self.deleted is False:
            self.deleted = True
            self.deleted_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def permanently_delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return ('<Project {}>'.format(self.name))
