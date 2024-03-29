#!/usr/bin/env python
# coding=utf-8

from flask import (url_for, Flask,
        render_template, session,
        redirect, abort, flash, request)
from flask_login import (LoginManager,
        logout_user, login_user,
        current_user, login_required)
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from datetime import timedelta

from admin.views import MV
from admin import blue_admin
from forms import LoginForm
from config import Config
from db import User

app = Flask('hydra')
bootstrap = Bootstrap()
bootstrap.init_app(app)
app.config.from_object(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
admin = Admin(app, name='Hail Hydra', template_mode='bootstrap3')
admin.add_view(MV(User))
app.register_blueprint(blue_admin)

#pymongo = PyMongo(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

# login expired time
app.permanent_session_lifetime = timedelta(minutes=120)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()

@app.route('/')
def index():
    if all([current_user.is_authenticated, current_user.is_active]):
        return redirect('/admin')
    else:
        return render_template('401.html'), 401

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        remember = form.remember.data
        user = User.objects(name=name, pwd=pwd).first()
        if user:
            flash('login success !', category='login success')
            login_user(user, remember=form.remember.data)
            return redirect('/admin')
        else:
            return render_template('login.html', form=form, status=1)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    return '[+]  searching'

@app.route('/test')
def test():
    return render_template('admin/x.html')

app.run(debug=1)
