#!/usr/bin/env python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length,EqualTo, URL

from db import User


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(max=20)])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField('Remember Me')
