#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from config import DevConfig

app = Flask('hydra')
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
mongo = MongoEngine(app)


class User(mongo.Document):
    id = mongo.IntField(primary_key=True, required=True, default=1)
    name = mongo.StringField(required=True, unique=True, default='admin')
    nike = mongo.StringField(required=True, default='admin')
    pwd = mongo.StringField(required=True, default='h4dr@')

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User:  %r>' % self.name


#class ScanLog(mongo.Document):
#    # 0: not start, 1: starting, 2: running, 4: finished, 5: terminated
#    status = mongo.IntField(default=0)
#
#
#class ScanResult(mongo.Document):
#    scan_log = mongo.ReferenceField(ScanLog)
#    results = mongo.ListField()
