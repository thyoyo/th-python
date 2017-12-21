#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from manage_config import config

mail = Mail()
db = SQLAlchemy()

login_manager = LoginManager()
# 设为'strong' 时，Flask-Login 会记录客户端IP，
# 地址和浏览器的用户代理信息，如果发现异动就登出用户。
login_manager.session_protection = 'strong'
# 登入视图, 在用户未登入的情况下试图访问一个 login_required 视图，
# Flask-Login 会 闪现一条消息并把他们重定向到登入视图
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    db.app = app
    mail.init_app(app)
    login_manager.init_app(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
