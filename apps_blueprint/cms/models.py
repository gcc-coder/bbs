#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:17
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: models.py
@Software: PyCharm
@Description:
"""
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPermission(object):
    # 255二进制表示全部权限
    ALL_PERMISSION  = 0b11111111
    # 访问者权限
    VISITOR         = 0b000000001
    # 帖子管理者
    POSTER          = 0b00000010
    # 评论管理者
    COMMENTER       = 0b00000100
    # 板块管理者
    BOADER          = 0b00001000
    # 前台用户管理者
    FRONTER         = 0b00010000
    # 后台用户管理者
    BACKER          = 0b00100000
    # 管理员权限
    # ADMIN           = 0b01000000

cms_role_user = db.Table('cms_role_user',
    db.Column('cmsrole_id', db.Integer, db.ForeignKey('cms_role.id')),
    db.Column('cmsuser_id', db.Integer, db.ForeignKey('cms_user.id'))
)

class CMSRole(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.now)
    permission = db.Column(db.Integer, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')

class CMSUser(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(60), nullable=True)
    _password = db.Column(db.String(110), nullable=True)
    email = db.Column(db.String(60), nullable=True)
    regist_time = db.Column(db.DateTime, default=datetime.now)

    # 由manage下的create_cms_user传参过来
    def __init__(self, username, password, email):
        self.username = username
        self.password = password    # 值password调用@password.setter中的加密方法
        self.email = email

    @property
    # 上面init中的self.password等于此方法
    def password(self):
        return self._password

    @password.setter
    # 加密password
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    """检查密码"""
    def check_password(self, raw_password):
        # self.password为数据库存储的加密密码，raw_password为表单提交的密码
        res = check_password_hash(self.password, raw_password)
        return res

    @property
    def permissions(self):
        # 判断用户是否属于某角色
        if not self.roles:
            return 0

        all_permissions = 0
        # 获取角色的所有权限
        for role in self.roles:
            # print(role)
            permissions = role.permission
            all_permissions |= permissions

        return all_permissions

    # 用户是否拥有传进来的权限
    def has_permission(self, permission):
        all_permissions = self.permissions

        result = all_permissions & permission == permission
        return result

    @property
    # 测试开发人员角色是否拥有全部权限
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)