#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:17
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: config.py
@Software: PyCharm
@Description:
"""
import os
from datetime import timedelta

DB_URI = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/bbs?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.urandom(16)
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)