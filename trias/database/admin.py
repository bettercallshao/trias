# -*- coding: utf-8 -*-
"""Admin routines."""


from sqlalchemy_utils import create_database, database_exists

from .table import Base, Room, Script, get_engine, get_session


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
            title="itza",
        ),
        Room(
            title="teo",
        )
    ]


def create_tables():

    engine = get_engine()

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)

    # Clear and recreate tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_samples():

    # Add sample rows
    session = get_session(get_engine())
    session.bulk_save_objects(sample_scripts())
    session.bulk_save_objects(sample_rooms())
    session.commit()
