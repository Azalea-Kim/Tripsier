# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/2 19:34
@Auth ： NIDO
@File ：forms.py
@IDE ：PyCharm
"""
from flask_wtf import FlaskForm
from wtforms import Form, StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, email


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

