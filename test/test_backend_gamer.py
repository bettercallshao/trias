# -*- coding: utf-8 -*-
"""Tests for worker module."""


from trias.backend import gamer
from trias.database.table import get_engine, get_session


def test_get_script():
    script = gamer.get_script(get_session(get_engine()))
    assert script.id > 0
    assert len(script.title) > 0
