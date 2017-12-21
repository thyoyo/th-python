#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db


class WxInfo(db.Model):
    """
    微信access_token和jsapi缓存
    """
    __tablename__ = 'wx_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String(1000))
    jsapi_ticket = db.Column(db.String(1000))
    create_time = db.Column(db.String(200))
