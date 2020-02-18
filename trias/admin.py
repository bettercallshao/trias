# -*- coding: utf-8 -*-
"""Flask app layer."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from ._table import Base, sample_scripts


def init_db():
    # Get connection string from env and create connection
    conn_str = os.getenv('CONN_STR')
    assert conn_str
    engine = create_engine(conn_str)

    # Create database
    if not database_exists(engine.url):
        create_database(engine.url)

    # Clear and recreate tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Add sample script rows
    session = sessionmaker(bind=engine)()
    for script in sample_scripts():
        session.add(script)
    session.commit()
