# -*- coding: utf-8 -*-
from functools import wraps

import requests
from flask import request, jsonify, session
import run_conf
from app2.service.tf_service import TFService

# 避免默认为开发模式
DEV_MODE = run_conf.dev_conf.get("mode")


def sso_auth(func):
    sso_url = 'http://sso.dianying.com/api/v1.0/checktoken?token='

    @wraps(func)
    def __auth(self):
        with self.app.app_context():
            # 判断时候为dev模式,如果是dev,不进行权限校验
            if DEV_MODE is True:
                return func(self)
            sso_token = request.args.get("sso_token") or request.cookies.get('sso_token')
            if sso_token is not None:
                r = requests.get(sso_url + sso_token)
                auth_info = r.json()
                # 如果用户的session状态还在，那么鉴权直接成功
                if session.get("user_id") is not None:
                    return func(self)
                if auth_info.get("error") is None:
                    # sso校验成功后的信息
                    uid = auth_info.get("user").get("uid")
                    tf_service = TFService(self.Session)
                    user = tf_service.get_user_info_by_user_id(uid)
                    if user is None:
                        return jsonify({"status": 998, "info": "ss"})
                    session["user_id"] = user.user_id
                    return func(self)
            return jsonify({"status": 999, "info": "ss"})  # 跳转到sso登录界面

    return __auth
