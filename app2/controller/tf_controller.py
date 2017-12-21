# coding:utf-8
from flask import request, jsonify, session
from app2.util.auth_tool import sso_auth
from app2.service.tf_service import TFService


class TFController:
    def __init__(self, sess, es, app, celery_app):
        self.Session = sess
        self.es = es
        self.app = app
        self.celery_app = celery_app
        self.cache = None

    @sso_auth
    def index(self):
        tf_service = TFService(self.Session, self.es)
        result = tf_service.get_user_info()

        # ES
        search_ = {'size': 30, 'stored_fields': ['_id'], "query": {"bool": {"must": []}},
                   "aggs": {request.form["aggs_name"]: {"terms": {"field": request.form["aggs_name"], "size": 10}}}}
        result2 = tf_service.get_result_by_search(search_)
        result3 = result2["aggregations"][request.form["aggs_name"]]

        # celery
        self.celery_app.send_task('tasks.add_user_log', args=[session.get("user_id"), ])

        return jsonify({"status": 0, "data": {"test": {"account": 1024, "user_id": 123456}}})

