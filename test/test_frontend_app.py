# -*- coding: utf-8 -*-
"""Tests for frontend app module."""

from trias.frontend.app import get_room, get_rooms


def test_get_rooms():
    rooms = get_rooms()
    assert len(rooms) == 2
    assert rooms[0].id == 1
    assert rooms[1].id == 2


def test_get_room():
    room = get_room(1)
    assert room.id == 1
