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
# from models import Users, Articles, Tags

manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()