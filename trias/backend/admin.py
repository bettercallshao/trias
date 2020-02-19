# -*- coding: utf-8 -*-
"""Admin routines."""

from . import roomer
from ..database.table import get_engine, get_session


def take_room():
    session = get_session(get_engine())
    roomer.take_room(session, 'admin')
