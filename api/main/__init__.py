from flask import Blueprint

from settings import routes

from .views import LoginView
from .views import RegistrationView
from .views import LogoutView
from .views import HomeView

main = Blueprint('main', __name__)

login = LoginView.as_view('login')
registration = RegistrationView.as_view('registration')
logout = LogoutView.as_view('logout')
home = HomeView.as_view('profile')


main.add_url_rule(routes.LOGIN, view_func=login, methods=['POST'])
main.add_url_rule(routes.REGISTRATION, view_func=registration, methods=['POST'])
main.add_url_rule(routes.LOGOUT, view_func=logout, methods=['POST'])
main.add_url_rule(routes.PROFILE, view_func=home, methods=['GET', 'PUT', 'DELETE'])
