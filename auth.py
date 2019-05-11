import os
from functools import wraps
from flask import g, request, jsonify, url_for
from db import Session
from models import User
import jwt

def generateToken(email):
    return jwt.encode({'email': email}, os.environ['PRIVATE_KEY'].encode('utf-8'), algorithm='RS256').decode('utf-8')


def verifyToken(token):
    try:
        data = jwt.decode(token, os.environ['PUBLIC_KEY'].encode('utf-8'), algorithms=['RS256'])
    except jwt.DecodeError:
        return None
    except jwt.InvalidTokenError:
        return None
    user = Session.query(User).filter(User.email == data['email']).first()
    return user


def verifyUser(username_or_token, password):
    user = verifyToken(username_or_token)
    if not user:
        user = Session.query(User).filter(User.email ==
                                          username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.method == 'OPTIONS':
            return jsonify({'errors' : 'Token is missing!'
                }), 401, {'Location': url_for('main.home', _external=True)}
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'errors' : 'Token is missing!'
                }), 401, {'Location': url_for('main.home', _external=True)}
        user = verifyToken(token)
        if not user:
            return jsonify({'errors': 'Unable to find user with those credentials.'
                }), 401, {'Location': url_for('main.home', _external=True)}
        g.user = user
        return f(*args, **kwargs)
    return decorated