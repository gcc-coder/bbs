#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:20
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: forms.py
@Software: PyCharm
@Description:
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length

class LoginForm(Form):
    email = StringField(validators=[Email(message='请输入正确的邮箱地址'), InputRequired(message='请输入邮箱地址')])
    password = StringField(validators=[Length(6, 20), InputRequired(message='请输入密码')])
    remember = IntegerField()