import os

from redis import Redis
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    # Production environment variables should be injected
    #   into the application
    mode = os.environ.get('FLASK_ENV')

    if mode == '':
        print("Error: No FLASK_ENV variable has been set.\n" +
              "eg. on Mac: export FLASK_ENV={development|production|testing}")
    elif mode == 'development':
        env_path = Path('./env_files') / 'development.env'
        load_dotenv(dotenv_path=env_path, verbose=True)
    elif mode == 'testing':
        env_path = Path('./env_files') / 'testing.env'
        load_dotenv(dotenv_path=env_path, verbose=True)

load_env()

class Config(object):
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_ENABLED = os.getenv('CSRF_ENABLED')
    SESSION_FILE_THRESHOLD = os.getenv('SESSION_FILE_THRESHOLD')
    MARSHMALLOW_SCHEMA_DEFAULT_JIT = 'toastedmarshmallow.Jit'

    # Database Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')

    # Session Config
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = os.getenv('SESSION_COOKIE_HTTPONLY')
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT')

    # Configure Redis Sessions
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')


    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'postgresql://{}:{}@{}/{}'.format(self.POSTGRES_USER, 
                                                 self.POSTGRES_PASSWORD, 
                                                 self.POSTGRES_HOST, 
                                                 self.POSTGRES_DB_NAME)

    @property
    def SESSION_REDIS(self):
        return Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)
