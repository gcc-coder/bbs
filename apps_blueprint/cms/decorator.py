#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/21 21:48
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: decorator.py
@Software: PyCharm
@Description:
"""
from flask import session, redirect, url_for, g
from functools import wraps

"""定义装饰器：判断访问的url是否为cms.login"""
def login_required(func):
    def index(*args, **kwargs):     # 此处函数名必须用index
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return index

"""定义装饰器传参数"""
def permission_required(permission):
    def outter(func):
        @wraps(func)    # 装饰器传参数时，需使用wraps进行装饰
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
