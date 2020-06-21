#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/6/20 19:49
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: email_captcha.py
@Software: PyCharm
@Description:
"""
import random
import string

"""生成字符串验证码"""
def generate_code(bit_num):
    '''
    :param bit_num: 生成验证码位数
    :return: 返回生成的验证码
    '''
    all_str = string.printable.split('!')[0]
    code = ''.join([random.choice(all_str) for i in range(bit_num)])
    return code