#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2020/5/15 11:17
@Author: Rick
@Contact：firelong.guo@hotmail.com 
@File: bbs_app.py
@Software: PyCharm
@Description:
"""
from flask import Flask
import config
from exts import db, mail
from apps_blueprint.cms.views import cms_bp
from apps_blueprint.common.views import common_bp
from apps_blueprint.front.views import front_bp
from flask_wtf import CSRFProtect

"""【目录结构】
cms - 后台
common - 共有
front - 前台
"""

app = Flask(__name__)
"""CSRFProtect用于保护网站：验证访问者是否为爬虫或含有csrf字符串的浏览器"""
CSRFProtect(app)    # CSRF可生成随机字符串，用于验证

app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

app.register_blueprint(cms_bp)
app.register_blueprint(common_bp)
app.register_blueprint(front_bp)

if __name__ == '__main__':
    app.run(debug=True)