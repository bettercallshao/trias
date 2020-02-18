# -*- coding: utf-8 -*-
"""Flask app layer."""

import os


from sqlalchemy import create_engine, update, select, func, text, or_, and_
from ._table import get_session, get_engine, Room
from uuid import uuid4
from random import random
from time import sleep
from logging import getLogger


def update_period():
    return 10


def take_room(session, worker_id):

    # Query 1 or 0 room with out dated timestamp
    find_query = select(
        [Room.id]
    ).where(
        or_(Room.worker == worker_id,
            Room.updated == None,
            Room.updated < (
                func.now() -
                text("interval '{} seconds'".format(update_period()))
            )),
    ).order_by(
        Room.id
    ).limit(
        1
    ).with_for_update()

    # Update room with our name
    update_query = update(
        Room
    ).values({
        Room.updated: func.now(),
        Room.worker: worker_id,
    }).where(
        Room.id == find_query.as_scalar()
    )

    update_proxy = session.execute(update_query)
    session.commit()

    if update_proxy.rowcount == 0:
        return None

    # Select back what we found
    result_query = select(
        [Room.id, Room.title]
    ).where(
        Room.worker == worker_id
    ).limit(
        1
    )

    result = session.execute(result_query).fetchone()
    return result


def keep_room(session, worker_id, room_id):
    # Update room current timestamp
    query = update(
        Room
    ).values({
        Room.updated: func.now(),
    }).where(
        and_(Room.worker == worker_id,
             Room.id == room_id)
    )
    proxy = session.execute(query)
    session.commit()

    return proxy.rowcount == 1


class Worker(object):
    def __init__(self):
        self.session = get_session(get_engine())
        self.id = str(uuid4())
        self.logger = getLogger('worker_' + self.id)

    def work(self):
        self.logger.log('Idle and waiting for work')
        room = None
        while not room:
            sleep(update_period() + 2 + random())
            room = take_room(self.session, self.id)

        room_id, room_title = room
        self.logger.log(f'Taking room id={room_id}, title={room_title}')

        while keep_room(self.session, self.id, room_id):
            sleep(update_period() + random())

        self.logger.log(f'Dropping room id={room_id}, title={room_title}')
        self.logger.log(f'Exiting')