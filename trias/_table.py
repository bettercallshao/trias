# -*- coding: utf-8 -*-
"""Script table definition."""

from sqlalchemy import Text, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Script(Base):
    __tablename__ = 'script'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    question = Column(Text)
    optiona = Column(Text)
    optionb = Column(Text)
    optionc = Column(Text)
    answer = Column(Text)


def sample_scripts():
    return [
        Script(
            title='Dragon Ball',
            question='What is 7 + 7',
            optiona='7',
            optionb='14',
            optionc='77',
            answer='b',
        ),
        Script(
            title='Canada Day',
            question='What is 7 + 1',
            optiona='71',
            optionb='17',
            optionc='8',
            answer='c',
        ),
    ]
