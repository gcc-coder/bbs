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
from flask import Blueprint, render_template, views, request, redirect, url_for
from apps_blueprint.cms.forms import LoginForm

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')

@cms_bp.route('/')
def index():
    return 'cms首页'

# 类视图：基于方法调度
class LoginView(views.MethodView):
    def get(self):
        return render_template('cms/login.html')

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            # 登录成功后，跳转首页
            return redirect(url_for('cms.font_index'))
        else:
            print(login_form.errors)
            return "邮箱或密码错误"

cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))