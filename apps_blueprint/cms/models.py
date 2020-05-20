#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:17
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: models.py
@Software: PyCharm
@Description:
"""
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class CMSUser(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(60), nullable=True)
    _password = db.Column(db.String(110), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    regist_time = db.Column(db.DateTime, default=datetime.now)

    # 由manage下的create_cms_user传参
    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email

    @property
    # 上面init中的self.password等于此方法
    def password(self):
        return self._password

    @password.setter
    # 加密password
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)