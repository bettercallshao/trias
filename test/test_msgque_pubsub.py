# -*- coding: utf-8 -*-
"""Tests for msgque module."""


import json
import threading
from time import sleep

import trias.msgque.pubsub as pubsub

key_a = 'key.a'


def test_basic():
    data = {
        'pub': {'a': 5},
        'sub': None,
    }

    def pub():
        channel = pubsub.get_channel(pubsub.get_connection())
        pubsub.publish(channel, key_a, json.dumps(data['pub']))

    def sub():
        channel = pubsub.get_channel(pubsub.get_connection())
        for msg in pubsub.consume(channel, key_a):
            if msg:
                data['sub'] = json.loads(msg)
                break

    t = threading.Thread(target=sub)
    t.start()
    sleep(0.2)
    pub()
    sleep(0.2)
    assert data['pub'] == data['sub']
