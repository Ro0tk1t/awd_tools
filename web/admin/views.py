#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint, render_template, request
from flask_admin import expose
from flask_restful import Resource, Api
from flask_login import current_user, login_required
from flask_admin.contrib.mongoengine import ModelView

import subprocess

from .forms import ScanForm
from db import User

blue_admin = Blueprint('blue_admin', 'hydra', url_prefix='/admin')
api = Api(blue_admin)

class MV(ModelView):
    #column_searchable_list = (User.name,)
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_active and current_user.name == 'admin':
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return self.login()

    @expose('/')
    def index(self):
        if all([current_user.is_authenticated, current_user.is_active]):
            return self.render('admin/index.html')
        else:
            return self.render('401.html'), 401


@blue_admin.route('/scan', methods=['GET', 'POST'])
def scan():
    form = ScanForm()
    if request.method == 'POST':# and form.validate_on_submit():
        ips = form.ips.data
        newpwd = form.newpwd.data
        oldpwd = form.oldpwd.data
        print(oldpwd)
        cmd = ['tony', '-e', ips, '-o', 'aaa', '-u', 'test', '-n', 'fdsfds']
        print(cmd)
        subprocess.Popen(cmd)
        return render_template('scan.html', form=form)
    return render_template('scan.html', form=form)


class HelloWorld(Resource):
    #@login_required
    def get(self):
        return {'Hello': 'World'}

api.add_resource(HelloWorld, '/hello')
