# -*- coding: utf-8 -*-
"""Backend room logic."""


from time import sleep
from random import random

from sqlalchemy import or_, and_, func, text, select, update

from ..database.table import Room


def update_period():
    """Heart beat period"""
    return 3


def take_room(session, worker_id):
    """Try to take a room"""
    # Query 1 or 0 room with out dated timestamp
    find_query = select(
        [Room.id]
    ).where(
        or_(Room.worker == worker_id,
            Room.updated == None, # noqa
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
    """Try to keep a room"""
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


def take_room_block(session, worker_id):
    """Blocks until a room is available"""
    while True:
        room = take_room(session, worker_id)
        if room:
            return room
        sleep(update_period() + 1 + random())


def keep_room_block(stop, session, worker_id, room_id):
    """Block and keep the room until we don't have a room"""
    while not stop() and keep_room(session, worker_id, room_id):
        sleep(update_period())
