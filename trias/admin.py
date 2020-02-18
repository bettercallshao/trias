# -*- coding: utf-8 -*-
"""Admin routines."""


from sqlalchemy_utils import create_database, database_exists

from .backend import _worker as worker
from .database.table import Base, get_engine, get_session, sample_rooms, sample_scripts


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
