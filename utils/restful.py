#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/6/11 22:54
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: restful.py
@Software: PyCharm
@Description:
"""
from flask import jsonify

class HttpCode(object):
    ok = 200
    bad_request = 400
    unauthorized = 401
    server_error = 500

# 定义规范
def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data})

# 定义各状态码返回信息
def success(message='', data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)

def bad_request_error(message=''):
    return restful_result(code=HttpCode.bad_request, message=message, data=None)

def unauthor_error(message=''):
    return restful_result(code=HttpCode.unauthorized, message=message, data=None)

def server_error(message=''):
    return restful_result(code=HttpCode.server_error, message=message or "服务器内部错误", data=None)