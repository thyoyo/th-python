#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by tianhua on 2016/9/1


import sys
from datetime import datetime
from flask import jsonify, g, request
from flask import redirect, url_for
from suds.client import Client
from app import db
from app.db_models.auth import User
from app.db_models.wx_info import WxInfo
from app.email import send_email
from app.main import main
from flask_login import login_user, current_user, logout_user
from sqlalchemy.sql.expression import func
from operator import and_


reload(sys)
sys.setdefaultencoding('utf-8')


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('static', filename='home.html'))
    else:
        return redirect(url_for('static', filename='login.html'))


@main.route('/login', methods=['POST'])
def login():
    request_data = request.json
    if request_data is None:
        request_data = request.form
    username = request_data.get("username")
    password = request_data.get("password")
    refer = request_data.get("refer")

    # 用户名密码登陆
    if username is None or password is None or username == '' or password == '':
        return jsonify({'code': '404', 'msg': 'error'})
    g.current_user = User.query.filter_by(username=username).first()

    return jsonify({
        'code': 200,
        'data': {
            'token': g.current_user.generate_auth_token(expiration=36000),
            'user': g.current_user.to_json(),
            'status': g.current_user.status,
            'refer': refer
        }
    })


@main.route('/list', methods=['GET'])
def list():
    now_time = datetime.datetime.now()
    day_now = now_time.strftime("%Y-%m-%d")
    day_before = (now_time - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    username_set = set()
    username_set.add('11')
    username_set.add('22')
    user_list = User.query.filter(func.find_in_set(User.username, username_set)).all()

    User.session.query(func.count('*').label('count'))\
        .group_by(func.DATE_FORMAT(User.update_time, '%Y/%m'))

    current_page = 1
    page_size = 10
    ids = [1, 2, 3]
    User.query.filter(and_(User.id.in_(ids)), User.name.in_(ids))\
        .outerjoin(WxInfo, User.id == WxInfo.id).add_entity(WxInfo)\
        .group_by(User.id) \
        .add_column(func.group_concat(User.name)) \
        .paginate(current_page, page_size)
