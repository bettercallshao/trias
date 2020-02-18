# -*- coding: utf-8 -*-
"""Script table definition."""

from sqlalchemy import Text, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    worker = Column(Text)
    updated = Column(DateTime)


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


def sample_rooms():
    return [
        Room(
            title = "itza"
        ),
        Room(
            title = "teo"
        )
    ]


def get_engine():
    # Get connection string from env and create connection
    conn_str = os.getenv('CONN_STR')
    assert conn_str
    return create_engine(conn_str)


def get_session(engine):
    return sessionmaker(bind=engine)()
