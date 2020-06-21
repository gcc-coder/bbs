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
from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from utils import cache_redis

# 创建Form基类：抽离出共用的message，其他有使用该message的进行继承即可。
class BaseForm(Form):
    def get_error(self):
        # message = reset_form.errors.popitem()[1][0]
        message = self.errors.popitem()[1][0]   # 类内部使用self
        return message

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱地址'), InputRequired(message='请输入邮箱地址')])
    password = StringField(validators=[Length(6, 20, message='密码长度不符合要求'), InputRequired(message='请输入密码')])
    remember = IntegerField()

class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='旧密码长度不符合要求')])
    newpwd = StringField(validators=[Length(6, 20, message='新密码长度不符合要求')])
    confirm_pwd = StringField(validators=[EqualTo("newpwd", message="两次密码不一致")])

class CaptchaForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱地址')])
    captcha = StringField(validators=[Length(4, 6, message="验证码不正确")])

    def validate_captcha(self, field):
        captcha = self.captcha.data     # 表单提交的验证码
        # captcha = field.data     # 表单提交的验证码
        email = self.email.data
        redis_captcha = cache_redis.captcha_get(email)      # 获取Redis存储的验证码

        if redis_captcha.lower() != captcha.lower():
            raise ValidationError("验证码不正确")