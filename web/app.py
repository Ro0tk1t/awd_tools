#!/usr/bin/env python
# coding=utf-8

from flask import ( url_for,
        Flask, render_template, session,
        redirect, abort, flash, request)
from flask_login import (LoginManager,
        logout_user, login_user,
        current_user, login_required)
from flask_admin import Admin
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

@login_manager.user_loader
def load_user(userid):
    return User.objects(id=userid).first()

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
        name = form.username.data
        pwd = form.password.data
        remember = form.remember.data
        user = User.objects(name=name, pwd=pwd).first()
        if user:
            session['user'] = user.name
            flash('login success !', category='login success')
            login_user(user, remember=form.remember.data)
            return redirect('/admin')
        else:
            return render_template('login.html', form=form, status=0)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    return '[+]  searching'

app.run(debug=1)
