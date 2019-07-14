#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
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

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User:  %r>' % self.name
