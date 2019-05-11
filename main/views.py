from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from marshmallow import ValidationError

# internal package imports
from .forms import UserRegistrationSchema
from db import Session
from models import User
from auth import generateToken, tokenRequired

main = Blueprint('main', __name__)

class Login(MethodView):
    """View to deal with user login flow."""
    def post(self):
        json_input = request.get_json()
        login_schema = UserRegistrationSchema(exclude=('first_name', 'last_name'))
        try:
            data = login_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        user = Session.query(User).filter_by(email=data['email']).first()
        if user is None:
            return jsonify({'errors': 'User with that email does not exist.'}), 422
        if not user.verify_password(data['password']):
            return jsonify({'errors': 'Email and password do not match.'}), 422
        g.user = user
        resp_object = {'email': g.user.email}
        return jsonify(resp_object), 201, {'Location': url_for('main.home', _external=True), 
                                            'Authorization': generateToken(g.user.email)}


class Registration(MethodView):
    """View to deal with user registration flow."""
    def post(self):
        json_input = request.get_json()
        user_schema = UserRegistrationSchema()
        try:
            data = user_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        user = Session.query(User).filter_by(email=data['email']).first()
        if user is not None:
            return jsonify({'errors': 'User with that email already exists.'}), 422
        user = User(**data)
        user.password = user.set_password(data['password'])
        Session.add(user)
        Session.commit()
        g.user = user
        resp_object = {'Email': g.user.email}
        return jsonify(resp_object), 201, {'Location': url_for('main.home', _external=True),
                                            'Authorization': generateToken(g.user.email)}


class Home(MethodView):
    decorators = [tokenRequired]
    def get(self):
        return jsonify({'message': 'You made it!'}), 201


home_view = Home.as_view('home')
login_view = Login.as_view('login')
register_view = Registration.as_view('registration')
main.add_url_rule('/home', view_func=home_view, methods=['GET'])
main.add_url_rule('/', view_func=login_view, methods=['POST'])
main.add_url_rule('/register', view_func=register_view, methods=['POST'])