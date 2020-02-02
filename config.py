# -*- coding: utf-8 -*-
"""Configuration classes for running application."""

import redis


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MARSHMALLOW_SCHEMA_DEFAULT_JIT = 'toastedmarshmallow.Jit'
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = False


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/tempdb'
    SESSION_REDIS = redis.Redis(host='localhost', port='6379')
    SECRET_KEY = b'\x01v,\xd4Dq\nN[\xc2x@\\\xd0\xde\xa7'
    SESSION_FILE_THRESHOLD = 1000


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/tempdb'
    SESSION_REDIS = redis.Redis(host='localhost', port='6379')
    SECRET_KEY = b'\x01v,\xd4Dq\nN[\xc2x@\\\xd0\xde\xa7'
    SESSION_FILE_THRESHOLD = 1000


app_config = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'default': 'config.DevelopmentConfig'
}
