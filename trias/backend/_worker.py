# -*- coding: utf-8 -*-
"""Backend worker."""

from time import sleep
from uuid import uuid4
from random import random
from logging import getLogger

from ..database.table import get_engine, get_session
from ._roomer import update_period, take_room, keep_room


class Worker(object):
    def __init__(self):
        self.session = get_session(get_engine())
        self.id = str(uuid4())
        self.logger = getLogger('worker_' + self.id)

    def work(self):
        self.logger.log('Idle and waiting for work')
        room = None
        while not room:
            sleep(update_period() + 1 + random())
            room = take_room(self.session, self.id)

        room_id, room_title = room
        self.logger.log(f'Taking room id={room_id}, title={room_title}')

        while keep_room(self.session, self.id, room_id):
            sleep(update_period())

        self.logger.log(f'Dropping room id={room_id}, title={room_title}')
        self.logger.log(f'Exiting')
