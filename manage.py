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
from apps_blueprint.cms.models import CMSUser

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


if __name__ == '__main__':
    manager.run()