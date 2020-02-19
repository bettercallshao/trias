# -*- coding: utf-8 -*-
"""Backend game logic."""


import json

from sqlalchemy import func

from ..game.trivia import Trivia
from ..msgque.pubsub import consume, publish, get_channel, get_connection
from ..database.table import Script, get_engine, get_session


def get_script(session):
    return session.query(
        Script
    ).order_by(
        func.random()
    ).first()


def game_block(stop, room_id):
    session = get_session(get_engine())
    game = Trivia(lambda: get_script(session))

    connection = get_connection()
    pub = get_channel(connection)
    sub = get_channel(connection)

    for recv in consume(sub, f'{room_id}.f2b'):
        if stop():
            break
        send = game.tick(json.loads(recv) if recv else None)
        if send:
            publish(pub, f'{room_id}.b2f', json.dumps(send))
