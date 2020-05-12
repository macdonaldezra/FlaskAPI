from flask import jsonify
from flask import request
from flask import url_for
from flask import g
from flask.views import MethodView
from marshmallow import ValidationError
from marshmallow import INCLUDE

from .forms import UserSchema
from .forms import UpdateUserSchema
from .forms import ConfirmUserPasswordSchema
from utils.auth import generate_session
from utils.auth import login_required
from utils.auth import remove_session
from models import User
from models import db


class LoginView(MethodView):
    """Validate a given user's and manage access to secure interface."""
    def post(self):
        # get json data from post request
        json_data = request.get_json()
        # initialize user login schema
        login_schema = UserSchema(exclude=['first_name', 'last_name', 'email', 'clients'])
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


class LogoutView(MethodView):
    """Remove a user's session from session table."""
    def post(self):
        remove_session()


class RegistrationView(MethodView):
    """Create a new user View to deal with user registration flow."""
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema(exclude=['clients'])
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
        
        resp_object = user_schema.dump(user)
        generate_session(user.username)
        return jsonify(resp_object), 201

class HomeView(MethodView):
    """Resource to allow user to manage their personal account."""
    decorators = [login_required]
    
    def get(self):
        """Retrieve information about a given user to endpoint."""
        user_schema = UserSchema()
        resp_object = user_schema.dump(g.user)
        return jsonify(resp_object), 202

    def put(self):
        """Update and validate a provided user's information."""
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

            # send verification email to client using desired API

            ret_vals = user_schema.dump(g.user)
            return jsonify(ret_vals), 202

        g.user.update(**data['user'])
        ret_vals = user_schema.dump(g.user)
        return jsonify(ret_vals), 202

    def delete(self):
        """Delete a user permanently from the database."""
        json_input = request.get_json()
        delete_schema = ConfirmUserPasswordSchema()
        try:
            data = delete_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        if not g.user.verify_password(data['confirm_password']):
            return jsonify({'errors': 'Username and password do not match.'}), 422
        g.user.permanently_delete()
        remove_session()
        return jsonify({'success': 'Account has been permanently deleted.'}), 308

