from flask import Blueprint, jsonify, g, request, url_for
from flask.views import MethodView
from marshmallow import ValidationError, pprint, INCLUDE

# internal package imports
from .forms import (UserSchema, UpdateUserSchema, ClientSchema, 
                    ConfirmUserPasswordSchema, ProjectSchema)
from auth import generate_session, login_required, remove_session
from models import db, User, Client, Project

main = Blueprint('main', __name__)

class LoginView(MethodView):
    """View to deal with user login flow."""
    def post(self):
        json_data = request.get_json() # get json data from post request
        login_schema = UserSchema(exclude=('first_name', 'last_name', 'email', 'clients')) # initialize data schema
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
    """Resource to allow user to logout."""
    def post(self):
        remove_session()

class RegistrationView(MethodView):
    """View to deal with user registration flow."""
    def post(self):
        json_data = request.get_json()
        user_schema = UserSchema(exclude=('clients'))
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
        
        resp_object = UserSchema.dumps()
        generate_session(user.username)
        return jsonify(resp_object), 201

class HomeView(MethodView):
    """Resource to allow user to manage their personal account."""
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
            # send verification email
            ret_vals = user_schema.dump(g.user)
            return jsonify(ret_vals), 202

        g.user.update(**data['user'])
        ret_vals = user_schema.dump(g.user)
        return jsonify(ret_vals), 202

    def delete(self):
        json_input = request.get_json()
        delete_schema = ConfirmUserPasswordSchema()
        try:
            data = delete_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        if not g.user.verify_password(data['confirm_password']):
            return jsonify({'errors': 'Password does not match your username.'}), 422
        g.user.permanently_delete()
        remove_session()
        return jsonify({'success': 'Account has been permanently deleted.'}), 308


class ClientsView(MethodView):
    """Resource to allow user to display clients."""
    decorators = [login_required]

    def get(self):
        clients_schema = ClientSchema(many=True)
        clients = g.user.get_clients()
        ret_vals = clients_schema.dump(clients)
        # make sure that returned value includes client projects
        return jsonify(ret_vals), 201

    def post(self):
        json_input = request.get_json()
        client_schema = ClientSchema()
        try:
            data = client_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422
        
        client = g.user.get_client(data['name'], data['email'])
        if client:
            return jsonify({'errors': 'Client with that name and email already exists.'}), 422

        client = Client(user=g.user, **data)
        g.user.clients.append(client)
        db.session.add(client)
        db.session.commit()

        clients = g.user.clients.all()
        ret_vals = ClientSchema().dump(clients, many=True)
        return jsonify({'clients' : ret_vals}), 201

class ClientView(MethodView):
    """Resource to allow user to manage a client."""
    decorators = [login_required]

    def get(self):
        """Get the current client and their projects."""
        json_input = request.get_json()
        try:
            client_name = json_input['client_name']
            client_email = json_input['client_email']
        except:
            return jsonify({'errors': 'Invalid data sent to this route.'}), 422

        client = g.user.get_client(client_name, client_email)
        if client is None:
            return jsonify({'errors': 'Client does not exist.'}), 422
        ret_vals = ClientSchema().dump(client)
        return jsonify(ret_vals), 201

    def put(self):
        """Update an existing clients information."""
        json_input = request.get_json()
        try:
            client_name = json_input['client_name']
            client_email = json_input['client_email']
        except:
            return jsonify({'errors': 'Invalid data sent to this route.'}), 422

        client = g.user.get_client(client_name, client_email)
        if client is None:
            return jsonify({'errors': 'Client does not exist.'}), 422

        client_schema = ClientSchema(partial=True, unknown=INCLUDE)
        try:
            data = client_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422

        client.update(**data)
        ret_vals = ClientSchema().dump(client)
        return jsonify(ret_vals), 202

    def post(self):
        """Create a new project for a given client."""
        json_input = request.get_json()
        try:
            client_name = json_input['client_name']
            client_email = json_input['client_email']
        except:
            return jsonify({'errors': 'Invalid data sent to this route.'}), 422
    
        client = g.user.get_client(client_name, client_email)
        if client is None:
            return jsonify({'errors': 'Client does not exist.'}), 422
        
        project_schema = ProjectSchema(unknown=INCLUDE)
        try:
            data = project_schema.load(json_input)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 422

        try:
            project = Project(client=client, **data)
            new_project = client.projects.append(project)
            db.session.add(new_project)
            db.session.commit()
            client = db.session.refresh(client)
        except:
            return jsonify({'errrors': 'Internal server error, unable to add project.'}), 422

        ret_vals = ClientSchema().dump(client)
        return jsonify(ret_vals), 202

    def delete(self):
        """Delete an existing client."""
        json_input = request.get_json()
        try:
            client_name = json_input['client_name']
            client_email = json_input['client_email']
        except:
            return jsonify({'errors': 'Invalid data sent to this route.'}), 422

        client = g.user.get_client(client_name, client_email)
        if client is None:
            return jsonify({'errors': 'Client does not exist.'}), 422
        client.delete()
        return jsonify({'success': 'Client has been successfully deleted.'}), 308


# Register views
login_view = LoginView.as_view('login')
register_view = RegistrationView.as_view('registration')
logout_view = LogoutView.as_view('logout')
home_view = HomeView.as_view('profile')
client_view = ClientView.as_view('client')
clients_view = ClientsView.as_view('clients')

# consider changing url parameters, profile, clients=username, client=client_name
main.add_url_rule('/', view_func=login_view, methods=['POST'])
main.add_url_rule('/register', view_func=register_view, methods=['POST'])
main.add_url_rule('/logout', view_func=logout_view, methods=['POST'])
main.add_url_rule('/profile', view_func=home_view, methods=['GET', 'PUT', 'DELETE'])
main.add_url_rule('/client', view_func=client_view, methods=['GET', 'PUT', 'POST', 'DELETE'])
main.add_url_rule('/clients', view_func=clients_view, methods=['GET', 'POST'])