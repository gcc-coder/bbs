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

TEMPLATES_AUTO_RELOAD = True

SECRET_KEY = os.urandom(16)
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

# 邮箱的发送地址
MAIL_SERVER = "smtp.189.cn"
# 端口465或587
MAIL_PORT = "465"
# MAIL_USE_TLS : default False  # 587端口
MAIL_USE_SSL = True
MAIL_USERNAME = "17710290729@189.cn"
MAIL_PASSWORD = "Dragon5572"
MAIL_DEFAULT_SENDER = "17710290729@189.cn"