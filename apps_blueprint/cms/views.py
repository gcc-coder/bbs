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

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

@cms_bp.route('/')
def index():
    return 'cms首页'