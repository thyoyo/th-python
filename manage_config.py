#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        pass
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dssdfsfdasdf'
    # 设为True时，每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky>@example.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/th_app'
    SQLALCHEMY_BINDS = {
        'th_app': 'mysql://root:root@127.0.0.1/th_app'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}