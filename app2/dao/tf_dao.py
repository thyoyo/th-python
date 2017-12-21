# coding : utf-8

from app2.bean.tf_bean import TFBean
from sqlalchemy import distinct
from sqlalchemy import asc
from elasticsearch import Elasticsearch, NotFoundError
from app2.util.cache_tool import cache_tool


class TFDao:
    def __init__(self, sess, es):
        self.session = sess
        self.es = es  # Elasticsearch(hosts=['127.0.0.1'], timeout=1000)
        self.index = 'maxwell_tf'
        self.doc_type = 'person'
        pass

    def get_user_info(self):
        self.session.query(distinct(TFBean.id)).all()
        self.session.query(TFBean).filter(TFBean.id == 1).all()
        return

    @cache_tool
    def get_result_by_search(self, search_):
        result = self.es.search(index=self.index, body=search_)
        return result

    def get_user_info_by_user_id(self, user_id):
        result = self.es.get(index=self.index, doc_type=self.doc_type, id=user_id)
        return result


if __name__ == '__main__':
    es = Elasticsearch(hosts=['127.0.0.1'], timeout=1000)
    tf_dao = TFDao(None, es)
    print tf_dao.get_user_info_by_user_id('cookie:11111')
