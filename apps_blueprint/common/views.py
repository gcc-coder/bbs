#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:20
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: views.py
@Software: PyCharm
@Description:
"""
from flask import Blueprint

common_bp = Blueprint('common', __name__, url_prefix='/common')

@common_bp.route('/')
def index():
    return 'common页面'