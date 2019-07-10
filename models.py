import jwt

import pytz
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
    clients = db.relationship('Client', backref='user', lazy='dynamic') # change backref='user'

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

    def check_deleted(self) -> bool:
        return self.deleted

    def delete(self):
        if self.deleted is False:
            self.deleted = True
            self.deleted_on = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def permanently_delete(self):
        db.session.delete(self)
        db.session.commit()

    def hash_password(self):
        hasher = PasswordHasher()
        self.password = hasher.hash(self.password)

    def verify_password(self, password: str) -> bool:
        try:
            hasher = PasswordHasher()
            hasher.verify(self.password, password)
            return True
        except VerifyMismatchError: # perhaps add messages later
            return False
        except InvalidHash:
            return False

    def generate_username_token(self, days: int = 1, seconds: int = 60) -> bool:
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
        try:
            data = jwt.decode(token, current_app.config['PUBLIC_KEY'].encode('utf-8'), algorithms=['RS256'])
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

    def generate_email_change_token(self, new_email: str, days: int = 1, seconds: int = 60) -> str:
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
        try:
            data = jwt.decode(token, current_app.config['PUBLIC_KEY'].encode('utf-8'), algorithms=['RS256'])
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
        return self.clients.filter_by(name=name, email=email).first()

    def get_clients(self):
        return self.clients.all()


class Client(db.Model):
    # Clients are unique by email and name.

    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(150))
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    projects = db.relationship('Project', backref='client', lazy='dynamic')
    deleted = db.Column(db.Boolean(), default=False)
    deleted_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # change users=user

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

# Still need to add an Email table as well
# Fields to include:
#   sent: boolean
#   subject: string
#   downloaded: string
#   recipients: string
#   message: string
#   received: boolean