from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from marshmallow import ValidationError, pprint

# internal package imports
from .forms import UserSchema, UpdateUserSchema
from auth import generateToken, tokenRequired
from models import User, db

main = Blueprint('main', __name__)


class Login(MethodView):
    """View to deal with user login flow."""
    def post(self):
        json_data = request.get_json() # get json data from post request
        login_schema = UserSchema(exclude=('first_name', 'last_name')) # initialize data schema
        try: # check for errors in form data
            data = login_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        # create new user
        user = User.query.filter_by(email=data['email']).first()
        if user is None:
            return jsonify({'errors': 'User with that email does not exist.'}), 422
        if not user.verify_password(data['password']):
            return jsonify({'errors': 'Email and password do not match.'}), 422
        resp_object = {'email': user.email}
        return jsonify(resp_object), 201, {'Location': url_for('main.profile', _external=True), 
                                            'Authorization': generateToken(user.email)}


class Registration(MethodView):
    """View to deal with user registration flow."""
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema()
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            return jsonify({'errors': 'User with that email already exists.'}), 422
        try:
            user = User(**data) # automatically assign dictionary values to object
            user.add()
        except:
            return jsonify({'errors': 'Unable to add user.'}), 422
        resp_object = {'email': user.email}
        return jsonify(resp_object), 201, {'Location': url_for('main.profile', _external=True),
                                            'Authorization': generateToken(user.email)}

class Home(MethodView):
    decorators = [tokenRequired]
    
    def get(self):
        return jsonify({'message': 'You made it!'}), 201

    def put(self):
        json_input = request.get_json()
        update_schema = UpdateUserSchema(partial=True)
        try:
            data = update_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422

        if 'new_password' in data:
            if not g.user.verify_password(data['user']['password']):
                return jsonify({'errors': 'Must enter proper current password.'}), 422
            g.user.password = data['new_password']
            g.user.hash_password()
            db.session.add(g.user)
            db.session.commit()
            user_schema = UserSchema()
            ret_vals = user_schema.dump(g.user)
            return jsonify(ret_vals), 202

        # update any other field
        g.user.update(**data['user'])
        user_schema = UserSchema()
        ret_vals = user_schema.dump(g.user)
        # ret_vals = update_schema.dump(g.user)
        return jsonify(ret_vals), 202

# Register views
home_view = Home.as_view('profile')
login_view = Login.as_view('login')
register_view = Registration.as_view('registration')
main.add_url_rule('/profile', view_func=home_view, methods=['GET', 'PUT'])
main.add_url_rule('/', view_func=login_view, methods=['POST'])
main.add_url_rule('/register', view_func=register_view, methods=['POST'])