class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\x01v,\xd4Dq\nN[\xc2x@\\\xd0\xde\xa7'


class TestingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/tempdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MARSHMALLOW_SCHEMA_DEFAULT_JIT = 'toastedmarshmallow.Jit'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/tempdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MARSHMALLOW_SCHEMA_DEFAULT_JIT = 'toastedmarshmallow.Jit'


app_config = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'default': 'config.DevelopmentConfig'
}
