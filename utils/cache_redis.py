#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/6/21 19:04
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: cache_redis.py
@Software: PyCharm
@Description:
"""
import redis

"""存储生成的验证码及其邮箱地址"""
# decode_responses为True则，value的数据类型为string（默认为二进制）
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def captcha_set(key, value, expire=60):     # 60秒后过期（清除key和value）
    r.set(key, value, expire)

def captcha_get(key):
    v = r.get(key)
    return v

# if __name__ == '__main__':
#     captcha_set('name', 'Rick')
#     print(captcha_get('name'))

