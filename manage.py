#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:17
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: manage.py
@Software: PyCharm
@Description:
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from bbs_app import app
# 导入模型
from apps_blueprint.cms.models import CMSUser, CMSRole, CMSPermission

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')

def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("CMS用户添加成功")

@manager.command
def create_role():  # 虚拟环境里执行命令 python manage.py create_role
    # 访问者
    visitor = CMSRole(role_name='访问者', desc='仅能查看数据，不能修改数据')
    visitor.permission = CMSPermission.VISITOR

    # 运营者
    operator = CMSRole(role_name='运营人员', desc='管理帖子，管理评论，管理前台用户')
    operator.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTER

    # 管理员
    admin = CMSRole(role_name='管理员', desc='全部权限')
    admin.permission = CMSPermission.ALL_PERMISSION

    # 开发人员
    developer = CMSRole(role_name='开发人员', desc='大部分权限')
    developer.permission = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTER | CMSPermission.BACKER

    # 添加到数据库
    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

# 测试用户是否有访问者权限
@manager.command
def test_permission():
    # user = CMSUser.query.first()    # 获取用户
    user = CMSUser.query.get(2)
    # print(user)
    if user.has_permission(CMSPermission.VISITOR):
        print('该用户拥有访问者权限')
    else:
        print('该用户没有访问者权限')

# 将用户(邮箱)添加到角色里
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(role_name=name).first()
        if role:
            # print(role.users)
            # 添加用户到角色 role.users为角色下面的用户列表
            role.users.append(user)     # users是模型CMSRole的外键
            db.session.commit()
            print("用户添加到角色成功")
        else:
            print("角色不存在")
    else:
        print("邮箱不存在")



if __name__ == '__main__':
    manager.run()