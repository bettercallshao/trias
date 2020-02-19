# -*- coding: utf-8 -*-
"""Backend worker."""

import sys
import signal
import logging
import threading
from time import sleep
from uuid import uuid4

from . import roomer
from ..database.table import get_engine, get_session


def work():
    """Entry point for backend work"""

    # Initialize
    session = get_session(get_engine())
    worker_id = str(uuid4())
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(logging.DEBUG)
    logger = logging.getLogger('worker_' + worker_id)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout)

    def log(msg):
        logger.info(msg)

    # Find a room to work on
    log('Idle and waiting for work')
    room_id, room_title = roomer.take_room_block(session, worker_id)
    log(f'Taking room id={room_id}, title={room_title}')

    # Thread stopping
    cancel = [False]

    def stop():
        return cancel[0]

    def signal_handler(sig, _):
        cancel[0] = True

    signal.signal(signal.SIGINT, signal_handler)

    # Start other threads
    threads = {
        'room': threading.Thread(
            target=roomer.keep_room_block,
            args=(stop, session, worker_id, room_id)
        ),
    }
    for key, thread in threads.items():
        thread.start()
        log(f'Started thread key={key} thread={thread}')

    # If any of child threads quit, we quit
    def is_all_alive():
        for key, thread in threads.items():
            if not thread.is_alive():
                log(f'Thread key={key} is terminated')
                return False
        return True

    while not stop() and is_all_alive():
        sleep(5)

    cancel[0] = True

    log(f'Dropping room id={room_id}, title={room_title}')
    log(f'Exiting')
