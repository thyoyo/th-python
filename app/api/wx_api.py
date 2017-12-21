#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from app import db
from app.api import api
from app.db_models.wx_info import WxInfo
from werkzeug.utils import redirect, secure_filename
from pypinyin import lazy_pinyin
from sqlalchemy.sql.expression import func
import sys
import random
import shutil
from datetime import datetime
import requests
import json
import time
from urllib import quote
import hashlib


reload(sys)
sys.setdefaultencoding('utf-8')


@api.route('/wx_api', methods=['GET'])
def get_wx_info():
    url = request.args.get('url', '')

    appid = 'test'
    secret = 'test'

    _wxinfo = WxInfo.query.order_by(WxInfo.id.desc()).first()
    if _wxinfo and time.time() - float(_wxinfo.create_time) < 7000:
        jsapi_ticket = _wxinfo.jsapi_ticket
    else:
        # 使用步骤：通过AppId和AppSecret请求accessToken,然后通过accessToken获取jsapi_ticket，生成config接口所需参数
        # accessToke 每日2000次，jsapi_ticket 每日100000次
        # access_token的存储至少要保留512个字符空间。access_token的有效期目前为2个小时，需定时刷新，重复获取将导致上次获取的access_token失效
        at_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, secret)
        access_token_result = requests.get(at_url)
        access_token = access_token_result.json().get('access_token', '')

        jt_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
        jsapi_ticket_result = requests.get(jt_url)
        jsapi_ticket = jsapi_ticket_result.json().get('ticket', '')

        _wxinfo = WxInfo(access_token=access_token, jsapi_ticket=jsapi_ticket, create_time=time.time())
        db.session.add(_wxinfo)
        db.session.commit()

    noncestr = create_noncestr()
    timestamp = int(time.time())  # 1489535486
    signature_parm = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (jsapi_ticket, noncestr, timestamp, url)
    signature = hashlib.sha1(signature_parm).hexdigest()

    return jsonify({
        'code': 200,
        'jsapi_ticket': jsapi_ticket,
        'url': url,
        'noncestr': noncestr,
        'timestamp': timestamp,
        'signature': signature,
        'appid': appid
    })


def create_noncestr(length=32):
    """产生随机字符串，不长于32位"""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    strs = []
    for x in range(length):
        strs.append(chars[random.randrange(0, len(chars))])
    return "".join(strs)

