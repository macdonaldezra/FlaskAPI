import os

from pathlib import Path

from flask import Flask
from flask_session import Session
from models import db
from config import Config

def create_app():
    app_config = Config()
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(app_config)
        Session(app)
        db.init_app(app)

        from main import main
        from user import user
        app.register_blueprint(main)
        app.register_blueprint(user)
    return app

app = create_app()