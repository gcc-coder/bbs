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
from flask import request, redirect, url_for, session
from .views import cms_bp

"""判断访问的url是否为login，若否，则跳转至login_url"""
@cms_bp.before_request  # 钩子函数
def before_request():
    # print(request.url, request.path)
    login_url = request.url.endswith(url_for('cms.login'))  # 返回布尔值
    # if request.path != url_for('cms.login'):
    if not login_url:
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('cms.login'))