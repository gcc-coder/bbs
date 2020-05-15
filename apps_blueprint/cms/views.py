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
from flask import Blueprint, render_template, views

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

@cms_bp.route('/')
def index():
    return 'cms首页'

class LoginView(views.MethodView):
    def get(self):
        return render_template('cms/cms_login.html')

cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))