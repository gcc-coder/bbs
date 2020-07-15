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
from apps_blueprint.cms.forms import LoginForm, ResetPwdForm, CaptchaForm
from apps_blueprint.cms.models import CMSUser, CMSPermission
from exts import db, mail
from utils import restful, email_captcha, cache_redis
from flask_mail import Message
from .decorator import login_required, permission_required
import re

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
            # msg = login_form.errors.popitem()[1][0]     # popitem()将errors信息转换为元组，再进行取值
            # return self.get(message=msg)
            # 将message抽离后的引入使用
            return self.get(message=login_form.get_error())

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
                # 需给ajax返回json类型的数据格式
                # return jsonify({"code": 200, "message": "密码修改成功"})
                return restful.success()    # 调用restful规范
            else:
                # return jsonify({"code": 400, "message": "旧密码错误"})
                return restful.bad_request_error(message="旧密码错误")

        else:
            # message = reset_form.errors.popitem()[1][0]
            # return jsonify({"code": 400, "message": message})
            return restful.bad_request_error(message=reset_form.get_error())    # 调用在forms定义的get_error

class ResetEmailView(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = CaptchaForm(request.form)
        if form.validate():
            email = form.email.data     # 表单提交的email
            # 查询数据库
            # res = CMSUser.query.filter_by(email=email).first()

            g.cms_user.email = email
            print(g.cms_user.email)
            db.session.commit()
            return restful.success()
        else:
            return restful.unauthor_error(form.get_error())

# 测试发送邮件
@cms_bp.route('/sendmail/')
def sendmail():
    msg = Message("Hello",
                  recipients=["1520128856@qq.com"],
                  body="邮件发送测试")
    mail.send(msg)
    return "邮件已发送！"

# 定义发送验证码邮件类视图
class EmailCaptcha(views.MethodView):
    def get(self):      # 对应ajax，此处仅用get
        email = request.args.get('email')
        # 验证邮箱地址是否合法
        pattern = re.compile(r'^[0-9a-zA-Z_]{5,19}@[0-9a-zA-Z]{1,13}\.')
        # 使用re库的match方法校验传入的邮箱参数是否合理,是否与表达式匹配
        if re.match(pattern, email) is not None:
        # if pattern.match(email):
            # 发送验证码邮件
            captcha = email_captcha.generate_code(4)
            msg = Message("cms验证码邮件", recipients=[email], body="您的验证码是：%s" % captcha)
            try:
                mail.send(msg)
            except:
                return restful.server_error()
            # 存储验证码到Redis，以及设置验证码过期时间
            cache_redis.captcha_set(email, captcha)
            return restful.success()
        else:
            return restful.bad_request_error("邮箱地址错误")


"""定义后台各板块路由"""
@cms_bp.route('/posts/')
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@cms_bp.route('/boards/')
@permission_required(CMSPermission.BOADER)
def boards():
    return render_template('cms/cms_boards.html')

@cms_bp.route('/fusers/')
@permission_required(CMSPermission.FRONTER)
def fusers():
    return render_template('cms/cms_fusers.html')

@cms_bp.route('/cusers/')
@permission_required(CMSPermission.BACKER)
def cusers():
    return render_template('cms/cms_cusers.html')

@cms_bp.route('/croles/')
# @permission_required(CMSPermission)
def croles():
    return render_template('cms/cms_croles.html')


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
cms_bp.add_url_rule('/resetpwd/', view_func=ResetPasswdView.as_view('resetpwd'))
cms_bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
cms_bp.add_url_rule('/email_captcha/', view_func=EmailCaptcha.as_view('email_captcha'))