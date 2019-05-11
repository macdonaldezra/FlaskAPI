import os

from flask import Flask
from config import app_config
import jwt

def configureRSA():
    inPrivateKey = open('instance/jwt-key')
    private_key = inPrivateKey.read()
    inPrivateKey.close()
    os.environ['PRIVATE_KEY'] = private_key

    inPublic = open('instance/jwt-key.pub')
    public_key = inPublic.read()
    inPublic.close()
    os.environ['PUBLIC_KEY'] = public_key


def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    configureRSA()
    from main.views import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    config_name = os.getenv('APP_SETTINGS')
    app = create_app(config_name)
    app.run(debug=True)
