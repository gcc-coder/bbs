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
from flask import (
    Blueprint,
    render_template,
    views,
    request,
    redirect,
    url_for,
    session,
    g,
    jsonify
)
from apps_blueprint.cms.forms import LoginForm, ResetPwdForm
from apps_blueprint.cms.models import CMSUser
from exts import db
# from .decorator import login_required     # 导入钩子函数

cms_bp = Blueprint('cms', __name__, url_prefix='/cms')
# 此行需写在cms_bp下面，因为导入的before_request，需要用到cms_bp
from .hooks import before_request   # 导入的钩子函数，用来判断访问的url是否为cms.login

@cms_bp.route('/')
# @login_required   # 该装饰器用来判断访问的url是否为cms.login，和钩子函数before_request二选一
def index():
    return render_template('cms/cms_index.html')

@cms_bp.route('/logout/')
def logout():
    # 清空session 与 重定向到登录页面
    session.clear()
    return redirect(url_for('cms.login'))

@cms_bp.route('/profile/')
def profile():
    return render_template('cms/cms_profile.html')

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
            # print(user.username)
            # user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id    # 设置session
                # session['user_name'] = user.username    # 设置session的user_name

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

class ResetPasswdView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        reset_form = ResetPwdForm(request.form)
        if reset_form.validate():
            oldpwd = reset_form.oldpwd.data
            confirm_pwd = reset_form.confirm_pwd.data
            # 获取用户对象
            user = g.cms_user
            if user.check_password(oldpwd):
                # 旧密码验证通过后，更新密码
                user.password = confirm_pwd
                db.session.commit()
                return jsonify({"code": 400, "message": "密码修改成功"})
            else:
                return jsonify({"code": 400, "message": "旧密码错误"})

        else:
            # 需给ajax返回json类型的数据格式
            message = reset_form.errors.popitem()[1][0]
            return jsonify({"code": 400, "message": message})

class ResetEmailView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass

cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
cms_bp.add_url_rule('/resetpwd/', view_func=ResetPasswdView.as_view('resetpwd'))
cms_bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))