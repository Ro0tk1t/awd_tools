#!/usr/bin/env python
# coding=utf-8

from flask import (
        Flask, render_template, session,
        redirect, abort, flash, request)
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from admin import blue_admin
from forms import LoginForm
from config import Config
from db import User

app = Flask('hydra')
bootstrap = Bootstrap()
bootstrap.init_app(app)
app.config.from_object(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
admin = Admin(app, name='hail hydra', template_mode='bootstrap3')
app.register_blueprint(blue_admin)

login_manager = LoginManager()
login_manager.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if 'user' in session:
        return redirect('/admin')
    else:
        return render_template('401.html'), 401

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        pwd = form.pwd.data
        remember = form.remember.data
        user = User.first_or_404(name=name, pwd=pwd)
        session['user'] = user.name
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/search')
def search():
    return '[+]  searching'

app.run(debug=1)
