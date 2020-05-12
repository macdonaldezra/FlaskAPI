from flask import Blueprint

from settings import routes
from .views import ClientView
from .views import ClientsView

user = Blueprint('user', __name__)

client = ClientView.as_view('client')
clients = ClientsView.as_view('clients')

user.add_url_rule(routes.CLIENT, view_func=client, methods=['GET', 'PUT', 'POST', 'DELETE'])
user.add_url_rule(routes.CLIENTS, view_func=clients, methods=['GET', 'POST'])