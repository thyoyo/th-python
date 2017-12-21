# coding:utf-8
# 标签工厂启动入口
from celery import Celery
from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app2.controller.tf_controller import TFController

from app2.controller.tag_info_controller import TagInfoController
from app2.controller.tags_factory2_controller import TagsFactory2Controller
from app2.controller.tags_factory_controller import TagsFactoryController
from app2.controller.tag_alldicts_controller import TagAllDictsController

import run_conf

MYSQL_HOST = run_conf.mysql_conf.get("host")
MYSQL_PORT = run_conf.mysql_conf.get("port")
MYSQL_USER = run_conf.mysql_conf.get("user")
MYSQL_PASSWORD = run_conf.mysql_conf.get("password")
ES_HOST = run_conf.es_conf.get("host")

# 避免初始化为开发模式
DEV_MODE = run_conf.dev_conf.get("mode") if run_conf.dev_conf.get("mode") else False

app = Flask(__name__)
app.secret_key = 'test'

if DEV_MODE is True:
    CORS(app, supports_credentials=True)
engine = create_engine('mysql+mysqlconnector://%s:%s@%s/test' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST),
                       echo=True,
                       encoding='utf8', pool_size=1, max_overflow=0)

Session = sessionmaker(bind=engine)
celery_app = Celery('tasks', broker=run_conf.celery_conf["MQ"], backend=run_conf.celery_conf["REDIS"])
celery_app.conf.task_default_queue = "tf_task"
celery_app.conf.event_queue_prefix = "tf_event"
es = Elasticsearch(hosts=ES_HOST, timeout=1000)

# 路由映射

tags_factory_controller = TagsFactoryController(Session, es, app, celery_app)
app.add_url_rule("/tags_factory/query_plan_by_user", view_func=tags_factory_controller.query_plans, methods=['GET'])
app.add_url_rule("/tags_factory/add_plan",
                 view_func=tags_factory_controller.add_plan, methods=['GET', 'POST'])
app.add_url_rule("/tags_factory/query_plan_by_plan_id",
                 view_func=tags_factory_controller.query_plan_by_plan_id, methods=['GET'])
app.add_url_rule("/tags_factory/query_users_by_tags_plan_detail",
                 view_func=tags_factory_controller.query_users_by_tags_plan_detail, methods=['GET', 'POST'])
app.add_url_rule("/tags_factory/query_users_by_tags_plan_id",
                 view_func=tags_factory_controller.query_users_by_tags_plan_id, methods=['GET'])
app.add_url_rule("/tags_factory/query_user_info_by_user_id",
                 view_func=tags_factory_controller.query_user_info_by_user_id, methods=['GET'])
app.add_url_rule('/tags_factory/get_car_product_attention',
                 view_func=tags_factory_controller.get_car_product_attention, methods=['POST'])
app.add_url_rule('/tags_factory/get_id_list_by_filter',
                 view_func=tags_factory_controller.get_id_list_by_filter, methods=['POST'])
app.add_url_rule('/tags_factory/get_person_group_by_filter',
                 view_func=tags_factory_controller.get_person_group_by_filter, methods=['POST'])
app.add_url_rule('/tags_factory/get_user_info_by_filter',
                 view_func=tags_factory_controller.get_user_info_by_filter, methods=['POST'])
app.add_url_rule('/tags_factory/add_collection',
                 view_func=tags_factory_controller.add_collection, methods=['POST'])
app.add_url_rule('/tags_factory/get_collection',
                 view_func=tags_factory_controller.get_collection, methods=['GET'])

# 标签基本信息
tag_info_controller = TagInfoController(Session, es)
app.add_url_rule("/tag/get_tag_info", view_func=tag_info_controller.get_tag_info, methods=['GET'])
app.add_url_rule("/tag/get_tag_dict", view_func=tag_info_controller.get_tag_dict, methods=['GET'])

tag_all_dicts_controller = TagAllDictsController(Session)
app.add_url_rule("/tag/get_level_dicts", view_func=tag_all_dicts_controller.get_level_dicts, methods=['GET'])
app.add_url_rule("/tag/get_model_to_names", view_func=tag_all_dicts_controller.get_model_to_names, methods=['GET'])
app.add_url_rule("/tag/get_makes", view_func=tag_all_dicts_controller.get_makes, methods=['GET'])

# 标签工厂2.0
tags_factory2_controller = TagsFactory2Controller(Session, es, celery_app)
app.add_url_rule("/v2/tags_factory/submit_task_query_user_info",
                 view_func=tags_factory2_controller.submit_task_query_user_info,
                 methods=['POST'])
app.add_url_rule("/v2/tags_factory/get_task_result",
                 view_func=tags_factory2_controller.get_task_result,
                 methods=['GET'])

# 人群预估
app.add_url_rule("/v2/tags_factory/submit_task_estimate_quantity",
                 view_func=tags_factory2_controller.submit_task_estimate_quantity,
                 methods=['POST'])

tf_controller = TFController(Session, es, app, celery_app)
app.add_url_rule("/index", view_func=tf_controller.index, methods=['GET'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
