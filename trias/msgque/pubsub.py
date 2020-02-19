# -*- coding: utf-8 -*-
"""RabbitMQ routines."""

import os

import pika


def timeout():
    return 1


def exchange():
    return 'trias'


def get_connection():
    host = os.getenv('RMQ_HOST')
    assert host
    return pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))


def get_channel(connection):
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange(), exchange_type='topic')
    return channel


def consume(channel, key):

    # Create temporary queue
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(
        exchange=exchange(), queue=queue_name, routing_key=key)

    for result in channel.consume(
            queue=queue_name, auto_ack=True, exclusive=True,
            inactivity_timeout=timeout()):
        if result:
            _, _, msg = result
            yield msg
        else:
            yield None


def publish(channel, key, msg):

    channel.basic_publish(
        exchange=exchange(), routing_key=key, body=msg)
