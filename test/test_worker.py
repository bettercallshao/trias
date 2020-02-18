# -*- coding: utf-8 -*-
"""Tests for worker module."""


from time import sleep

from trias.admin import init_db
from trias.database.table import get_engine, get_session
from trias.backend._worker import keep_room, take_room, update_period

worker_a = 'test_a'
worker_b = 'test_b'
worker_c = 'test_c'


def test_take_room():

    init_db()
    session = get_session(get_engine())

    room_a = take_room(session, worker_a)
    assert room_a == (1, 'itza')
    room_b = take_room(session, worker_b)
    assert room_b == (2, 'teo')
    assert not take_room(session, worker_c)


def test_keep_room():
    init_db()
    session = get_session(get_engine())

    room_id, _ = take_room(session, worker_a)
    assert keep_room(session, worker_a, room_id)

    sleep(update_period() + 1)

    take_room(session, worker_b)
    assert not keep_room(session, worker_a, room_id)
