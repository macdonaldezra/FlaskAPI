from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from marshmallow import ValidationError, pprint

# internal package imports
from .forms import UserSchema, UpdateUserSchema
from auth import generate_session, login_required, remove_session
from models import User, db

import sys

main = Blueprint('main', __name__)

class Login(MethodView):
    """View to deal with user login flow."""
    def post(self):
        json_data = request.get_json() # get json data from post request
        login_schema = UserSchema(exclude=('first_name', 'last_name', 'email')) # initialize data schema
        try: # check for errors in form data
            data = login_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        # create new user
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            return jsonify({'errors': 'User with that username does not exist.'}), 422
        if not user.verify_password(data['password']):
            return jsonify({'errors': 'Username and password do not match.'}), 422
        user_schema = UserSchema()
        resp_object = user_schema.dumps(user)
        generate_session(user.username)
        return jsonify(resp_object), 201

class Logout(MethodView):
    """Resource to allow user to logout."""
    def post(self):
        remove_session()

class Registration(MethodView):
    """View to deal with user registration flow."""
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        user = User.query.filter_by(username=data['username']).first()
        if user is not None:
            return jsonify({'errors': 'User with that username already exists.'}), 422
        try:
            user = User(**data) # automatically assign dictionary values to object
            user.add()
        except:
            return jsonify({'errors': 'Unable to add user.'}), 422
        resp_object = user_schema.dumps(user)
        generate_session(user.username)
        return jsonify(resp_object), 201

class Home(MethodView):
    decorators = [login_required]
    
    def get(self):
        user_schema = UserSchema()
        resp_object = user_schema.dump(g.user)
        return jsonify(resp_object), 202

    def put(self):
        json_input = request.get_json()
        update_schema = UpdateUserSchema(partial=True)
        try:
            data = update_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422

        user_schema = UserSchema()
        if 'new_password' in data:
            if not g.user.verify_password(data['user']['password']):
                return jsonify({'errors': 'Must enter proper current password.'}), 422
            g.user.password = data['new_password']
            g.user.hash_password()
            db.session.add(g.user)
            db.session.commit()
            ret_vals = user_schema.dump(g.user)
            return jsonify(ret_vals), 202

        if 'email' in data:
            g.user.generate_email_change_token(data['email'])
            ret_vals = user_schema.dump(g.user)
            return jsonify(ret_vals), 202

        g.user.update(**data['user'])
        ret_vals = user_schema.dump(g.user)
        return jsonify(ret_vals), 202




# Register views
home_view = Home.as_view('profile')
login_view = Login.as_view('login')
register_view = Registration.as_view('registration')
logout_view = Logout.as_view('logout')

main.add_url_rule('/profile', view_func=home_view, methods=['GET', 'PUT'])
main.add_url_rule('/', view_func=login_view, methods=['POST'])
main.add_url_rule('/register', view_func=register_view, methods=['POST'])
main.add_url_rule('/logout', view_func=logout_view, methods=['POST'])
