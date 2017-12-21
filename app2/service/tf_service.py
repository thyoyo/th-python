from app2.dao.tf_dao import TFDao
from elasticsearch import NotFoundError


class TFService:
    def __init__(self, session, es):
        self.Session = session
        self.es = es

    def get_user_info(self):
        dao = TFDao(self.Session())
        info = dao.get_user_info()
        self.Session().close()
        return info

    def get_result_by_search(self, search_):
        dao = TFDao(self.Session, self.es)
        result = dao.get_result_by_search(search_)
        return result

    def get_user_info_by_user_id(self, user_id):
        dao = TFDao(self.Session, self.es)
        try:
            result = dao.get_user_info_by_user_id(user_id)
            return result['_source']
        except NotFoundError as nfe:
            return {}
