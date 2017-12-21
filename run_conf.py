# -*- coding: utf-8 -*-

# 配置文件, 使用python文件, 更方便些
mysql_conf = dict()
es_conf = dict()
redis_conf = dict()
dev_conf = dict()
optimize = dict()
cache_conf = dict()
celery_conf = dict()
# 开发/线上 切换开关
dev_conf["mode"] = True

# 开发环境配置
if dev_conf["mode"] is True:
    mysql_conf["host"] = "127.0.0.1"
    mysql_conf["port"] = 3306
    mysql_conf["user"] = "test"
    mysql_conf["password"] = "test"
    mysql_conf["db"] = "test"
    es_conf["host"] = ['127.0.0.1']
    es_conf["port"] = 9200
    redis_conf["host"] = "127.0.0.1"
    optimize["compress"] = True
    optimize["cache"] = True
    cache_conf["EXPIRE_SEC"] = 6 * 60 * 60  # 缓存过期时间为6个小时
    celery_conf["MQ"] = "pyamqp://guest:@127.0.0.1//"  # rabbit mq
    celery_conf["REDIS"] = "redis://127.0.0.1"  # 存储celery执行结果

# 线上环境配置
if dev_conf["mode"] is False:
    mysql_conf["host"] = "127.0.0.1"
    mysql_conf["port"] = 3306
    mysql_conf["user"] = "test"
    mysql_conf["password"] = "test"
    mysql_conf["db"] = "test"
    es_conf["host"] = ['127.0.0.1']
    es_conf["port"] = 9200
    redis_conf["host"] = "127.0.0.1"
    optimize["compress"] = True
    optimize["cache"] = True
    cache_conf["EXPIRE_SEC"] = 6 * 60 * 60  # 缓存过期时间为6个小时
    celery_conf["MQ"] = "pyamqp://guest:@127.0.0.1//"  # rabbit mq
    celery_conf["REDIS"] = "redis://127.0.0.1"  # 存储celery执行结果
