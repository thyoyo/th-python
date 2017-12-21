# coding:utf-8
from contextlib import contextmanager
from mysql.connector.pooling import MySQLConnectionPool
import run_conf


@contextmanager
def get_cnx(cnx_pool):
    # 暂时没有处理异常
    cnx = cnx_pool.get_connection()
    c = cnx.cursor()
    yield cnx, c
    c.close()
    cnx.close()


class CacheFilter:
    def __init__(self, cnx_pool):
        self.cnx_pool = cnx_pool

    def add_cache_filter(self, filter_md5, _filter):
        with get_cnx(self.cnx_pool) as (cnx, c):
            _sql = ("INSERT INTO cache_filter (fid,filter) VALUES (%s,%s) "
                    "ON DUPLICATE KEY UPDATE times=times+1;")
            c.execute("set session transaction isolation level read uncommitted;")
            c.execute(_sql, (filter_md5, _filter))
            cnx.commit()

    def add_user_log(self, user_id):
        with get_cnx(self.cnx_pool) as (cnx, c):
            _sql = ("INSERT INTO user_log (user_id) VALUES (%s) "
                    "ON DUPLICATE KEY UPDATE times=times+1;")
            c.execute("set session transaction isolation level read uncommitted;")
            c.execute(_sql, (user_id,))
            cnx.commit()


if __name__ == '__main__':
    dbconfig = {
        "host": run_conf.mysql_conf.get("host"),
        "database": "test_db",
        "user": run_conf.mysql_conf.get("user"),
        "password": run_conf.mysql_conf.get("password")
    }
    cnx_pool = MySQLConnectionPool(pool_name='test_pool', pool_size=1, **dbconfig)
    cache_filter = CacheFilter(cnx_pool)
    cache_filter.add_user_log(9999)
