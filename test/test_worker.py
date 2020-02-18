# -*- coding: utf-8 -*-
"""Tests for worker module."""


from trias.admin import init_db
from trias.backend._worker import take_room, keep_room, update_period
from trias.database.table import get_engine, get_session
from time import sleep


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
    assert take_room(session, worker_c) == None


def test_keep_room():
    init_db()
    session = get_session(get_engine())

    room_id, _ = take_room(session, worker_a)
    assert keep_room(session, worker_a, room_id)

    sleep(update_period() + 1)

    take_room(session, worker_b)
    assert keep_room(session, worker_a, room_id) == False
