#!/usr/bin/env python
# coding=utf-8

from flask import Blueprint
from flask_admin import expose
from flask_login import current_user, login_required
from flask_admin.contrib.mongoengine import ModelView

from db import User

blue_admin = Blueprint('blue_admin', 'hydra', url_prefix='/admin')

class MV(ModelView):
    column_searchable_list = (User.name,)
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
    @login_required
    def index(self):
        if all([current_user.is_authenticated, current_user.is_active]):
            return self.render('admin/index.html')
        else:
            return render_template('401.html'), 401

