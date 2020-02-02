# -*- coding: utf-8 -*-
"""Authentication utility functions."""

from functools import wraps
from flask import g, jsonify, url_for, session
from models import User

def generate_session(username):
    session['username'] = username

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            user = User.query.filter_by(username=session['username']).first()
            if user is None:
                return jsonify({'errors': 'Invalid username was provided.'}), 401
            g.user = user
        else:
            return jsonify({'errors' : 'Insufficient credentials provided.'}), 401
        return f(*args, **kwargs)
    return decorated


def remove_session():
    session.pop('username', None)