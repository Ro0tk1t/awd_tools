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
    id = mongo.IntField(required=True, unique=True, default=1)
    name = mongo.StringField(required=True, unique=True, default='admin')
    pwd = mongo.StringField(required=True, default='h4dr@')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User:  %r>' % self.name
