#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint
from db import mongo

blue_admin = Blueprint('blue_admin', 'hydra', url_prefix='/admin')

@blue_admin.route('/test')
def test():
    return 'hhhhhhhhhhhhh'
