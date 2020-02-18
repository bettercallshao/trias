# -*- coding: utf-8 -*-
"""Admin routines."""

import os

from sqlalchemy import create_engine, update, select, func, text, or_
from sqlalchemy_utils import create_database, database_exists

from ._table import Base, sample_scripts, sample_rooms, Room, get_engine, get_session
from . import _worker as worker



def init_db():

    engine = get_engine()

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)

    # Clear and recreate tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Add sample rows
    session = get_session(engine)
    session.bulk_save_objects(sample_scripts())
    session.bulk_save_objects(sample_rooms())
    session.commit()


def take_room():
    session = get_session(get_engine())
    print(worker.take_room(session, 'admin'))