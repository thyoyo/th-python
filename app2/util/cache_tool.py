# coding:utf-8
import hashlib
import json
import zlib
from functools import wraps

import redis

from run_conf import optimize
from run_conf import redis_conf

redis_host = redis_conf.get("host")
client_pool = redis.ConnectionPool(host=redis_host, port=6379, db=0)
client = redis.StrictRedis(connection_pool=client_pool)
CACHE_PREFIX = "TF"  # 前缀
EXPIRE_SEC = 6 * 60 * 60  # 缓存过期时间为6小时


def cache_tool(func):
    @wraps(func)
    def __cache(self, arg):
        # 对筛选条件md5签名
        m2 = hashlib.md5()
        m2.update(json.dumps(arg))
        md5sum = m2.hexdigest()
        key = CACHE_PREFIX + md5sum
        compress = optimize["compress"]
        result = client.get(key)
        if result is not None:
            return json.loads(zlib.decompress(result)) if compress else json.loads(result)
        result = func(self, arg)
        data = zlib.compress(json.dumps(result)) if compress else json.dumps(result)
        client.set(key, data, ex=EXPIRE_SEC)
        return result

    return __cache
