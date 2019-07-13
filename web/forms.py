#!/usr/bin/env python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length,EqualTo, URL

from db import User


class LoginForm(FlaskForm):
    name = StringField("Username", [DataRequired(), Length(max=20)])
    pwd = StringField("Password", [DataRequired()])
    remember = BooleanField('Remember Me')
