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
from flask import Blueprint, render_template

front_bp = Blueprint('front', __name__)

@front_bp.route('/')
def index():
    return render_template('front_index.html')