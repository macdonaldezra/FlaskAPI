from functools import wraps
from flask import g, request, jsonify, url_for, current_app
from models import User, db
import jwt

def generateToken(email):
    return jwt.encode({'email': email}, current_app.config['PRIVATE_KEY'].encode('utf-8'), algorithm='RS256').decode('utf-8')

def verifyToken(token):
    try:
        data = jwt.decode(token, current_app.config['PUBLIC_KEY'].encode('utf-8'), algorithms=['RS256'])
    except jwt.DecodeError:
        return None
    except jwt.InvalidTokenError:
        return None
    user = User.query.filter_by(email=data['email']).first()
    return user

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'errors' : 'Token is missing!'}
                ), 401, {'Location': url_for('main.profile', _external=True)}
        user = verifyToken(token)
        if not user:
            return jsonify({'errors': 'An invalid authorization token was provided.'
                }), 401, {'Location': url_for('main.profile', _external=True)}
        g.user = user
        return f(*args, **kwargs)
    return decorated