#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime

from flask import current_app, request, url_for, g
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.Integer, default=1, nullable=False)
    name = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    @property
    def password(self):
        """
        password属性函数
        不允许直接读取原始值
        """
        raise AttributeError('密码是不可读属性')

    @password.setter
    def password(self, password):
        """
        设置密码hash值
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        将用户输入的密码明文与数据库比对
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    # 状态：0：关闭；1：启用；2：管理员；3：注册中
    def is_admin(self):
        if self.status == 2:
            return True
        else:
            return False

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'member_since': self.member_since.strftime("%Y-%m-%d %H:%M:%S"),
            'last_seen': self.last_seen.strftime("%Y-%m-%d %H:%M:%S")
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def from_json(json_user):
        email = json_user.get('email')
        username = json_user.get('username')
        name = json_user.get('name')
        member_since = json_user.get('member_since')
        last_seen = json_user.get('last_seen')
        return User(email=email, username=username, name=name, member_since=member_since, last_seen=last_seen)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
