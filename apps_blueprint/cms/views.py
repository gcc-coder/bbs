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
from flask import Blueprint, render_template, views, request, redirect, url_for, session
from apps_blueprint.cms.forms import LoginForm
from apps_blueprint.cms.models import CMSUser
from .decorator import login_required

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')
# 此行需写在cms_bp下面，因为导入的before_request，需要用到cms_bp
# from .hooks import before_request   # 导入的钩子函数，用来判断访问的url是否为cms.login

@cms_bp.route('/')
@login_required   # 该装饰器用来判断访问的url是否为cms.login
def index():
    return render_template('cms/cms_index.html')

# 类视图：基于方法调度
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            """数据库验证"""
            email = request.form.get('email')   # 等同于login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data

            user = CMSUser.query.filter(CMSUser.email == email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id    # 设置session
                # 记住密码
                if remember:
                    session.permanent = True    # 持久化
                # 登录成功后，跳转首页
                return redirect(url_for('cms.index'))  # 因是在蓝图中，所以格式为：蓝图名.函数
            else:
                # return render_template('cms/cms_login.html', message='邮箱或密码错误')
                return self.get(message='邮箱或密码错误')  # 为避免重复使用render，可使用给get传参的方式
        else:
            # return "登录表单验证未通过"
            msg = login_form.errors.popitem()[1][0]     # popitem()将errors信息转换为元组，再进行取值
            return self.get(message=msg)

cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))