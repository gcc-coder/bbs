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

class CMSUser(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    regist_time = db.Column(db.DateTime, default=datetime.now)