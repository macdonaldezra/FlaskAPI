class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = b'\x01v,\xd4Dq\nN[\xc2x@\\\xd0\xde\xa7'

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_URL = 'postgresql://postgres:password@localhost/tempdb'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_URL = 'postgresql://postgres:password@localhost/tempdb'


app_config = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'default': 'config.DevelopmentConfig'
}
