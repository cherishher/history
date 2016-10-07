# -*- coding: utf-8 -*-
# @Date    : 2016/5/24  19:56
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Answer(Base):
    __tablename__ = 'answer_situation'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    goal = Column(Integer,default=0)
    chance = Column(Integer,default=1)
    time = Column(Integer,default=0)
    answer = Column(String(128))
    questionList = Column(String(1024))

if __name__ == '__main__':
    Base.metadata.create_all(engine)