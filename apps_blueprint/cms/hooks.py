#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/21 21:57
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: hooks.py
@Software: PyCharm
@Description:
"""
from flask import request, redirect, url_for, session, g
from .views import cms_bp
from .views import CMSUser

"""判断访问的url是否为login，若否，则跳转至login_url"""
@cms_bp.before_request  # 钩子函数,在每次请求之前都会执行
def before_request():
    # print(request.url, request.path)
    login_url = request.url.endswith(url_for('cms.login'))  # 返回布尔值
    # if request.path != url_for('cms.login'):
    if not login_url:
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('cms.login'))

    if 'user_id' in  session:
        user = session.get('user_name')
        # user_id = CMSUser.query.get('user_id')
        # user =
        if user:
            g.cms_user = user
