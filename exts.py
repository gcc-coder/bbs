#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:18
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: exts.py
@Software: PyCharm
@Description:
"""
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()