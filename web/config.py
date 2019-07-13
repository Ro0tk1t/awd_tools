#!/usr/bin/env python
# coding=utf-8

class Config(object):
    SECRET_KEY = 'e5895216f74869ce2768d7dc2244184a'
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    @staticmethod
    def init_app(app):
        pass

class DevConfig(object):
    MONGODB_SETTINGS = {
        'db': 'hydra',
        'host': 'localhost',
        'port': 27017
    }
