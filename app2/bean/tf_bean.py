# coding:utf-8
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TFBean(Base):
    __tablename__ = 'tf_test'
    id = Column(Integer, primary_key=True)
    name = Column(String)