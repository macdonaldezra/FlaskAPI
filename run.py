from flask import Flask
from flask_session import Session
from models import db
from config import app_config

def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    with app.app_context():
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
        Session(app)
        db.init_app(app)

        from main.views import main
        app.register_blueprint(main)
        from file_manager.views import file_manager
        app.register_blueprint(file_manager)
    return app

if __name__ == '__main__':
    # Always set FLASK_ENV=development before testing
    app = create_app()
    app.run(debug=True, use_reloader=True)
