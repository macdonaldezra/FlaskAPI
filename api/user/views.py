from flask import jsonify
from flask import request
from flask import url_for
from flask import g
from flask.views import MethodView
from marshmallow import ValidationError
from marshmallow import INCLUDE

from utils.auth import generate_session
from utils.auth import login_required
from utils.auth import remove_session
from models import Project
from models import Client
from models import db
from .forms import ProjectSchema
from .forms import ClientSchema


class ClientsView(MethodView):
    """Resource to allow user to display clients."""
    decorators = [login_required]

    def get(self):
        """Retrieve a list of clients for a given user."""
        clients_schema = ClientSchema(many=True)
        clients = g.user.get_clients()
        ret_vals = clients_schema.dump(clients)
        return jsonify(ret_vals), 201


    def post(self):
        """Retrieve a list of clients for a given user."""
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

