# -*- coding: utf-8 -*-
"""Script table definition."""

import os

from sqlalchemy import Text, Column, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
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


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    worker = Column(Text)
    updated = Column(DateTime)


def get_engine():
    # Get connection string from env and create connection
    conn_str = os.getenv('CONN_STR')
    assert conn_str
    return create_engine(conn_str)


def get_session(engine):
    return sessionmaker(bind=engine)()
