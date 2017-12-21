# # -*- coding: utf-8 -*-
import json

from celery import Celery
from elasticsearch import Elasticsearch
from mysql.connector.pooling import MySQLConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from run_conf import celery_conf, es_conf, mysql_conf
from app2.service.tf_service import TFService
from app2.util.db import CacheFilter

import run_conf

celery_app = Celery('tasks', broker=celery_conf["MQ"], backend=celery_conf["REDIS"])
celery_app.conf.task_default_queue = "tf_task"
celery_app.conf.event_queue_prefix = "tf_event"

es = Elasticsearch(hosts=es_conf["host"], timeout=1000)
sqlalchemy_conn = 'mysql+mysqlconnector://%s:%s@%s/tags_factory' % (mysql_conf["user"], mysql_conf["password"], mysql_conf["host"])
engine = create_engine(sqlalchemy_conn, echo=True, encoding='utf8', pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)
dbconfig = {
    "host": run_conf.mysql_conf.get("host"),
    "database": "tags_factory",
    "user": run_conf.mysql_conf.get("user"),
    "password": run_conf.mysql_conf.get("password")
}
cnx_pool = MySQLConnectionPool(pool_name='task_pool', pool_size=5, **dbconfig)


# 记录用户的登录次数 首次/最近登录时间
# 将需要缓存的filter加入mysql
@celery_app.task(name='tasks.add_user_log')
def add_user_log(user_id):
    cache_filter = CacheFilter(cnx_pool)
    cache_filter.add_user_log(user_id)


@celery_app.task(name='tasks.get_user_info')
def get_user_info():
    tf_service = TFService(Session, es)
    result = tf_service.get_user_info()
    return result


if __name__ == '__main__':
    add_user_log(8888)
