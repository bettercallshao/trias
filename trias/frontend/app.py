# -*- coding: utf-8 -*-
"""Flask app layer."""

import os

from flask import Flask, render_template
from gevent import Timeout
from flask_sockets import Sockets

from ..msgque.pubsub import consume, publish, get_channel, get_connection
from ..database.table import Room, get_engine, get_session

engine = get_engine()
connection = get_connection()

app = Flask('trias', root_path=os.path.dirname(__file__))
sockets = Sockets(app)


def get_rooms():
    session = get_session(engine)
    result = session.query(
        Room
    ).order_by(
        Room.id
    ).all()
    session.close()
    return result


def get_room(room_id):
    session = get_session(engine)
    result = session.query(
        Room
    ).filter(
        Room.id == room_id
    ).first()
    session.close()
    return result


@app.route('/')
def home():
    return render_template('home.html', rooms=get_rooms())


@app.route('/room/<room_id>')
def room(room_id):
    return render_template('room.html', room=get_room(room_id))


@sockets.route('/ws/<room_id>')
def ws(socket, room_id):
    pub = get_channel(connection)
    sub = get_channel(connection)
    while not socket.closed:
        for b2f in consume(sub, f'{room_id}.b2f'):
            if b2f:
                socket.send(str(b2f))
            with Timeout(0.2, False):
                f2b = socket.receive()
                if f2b:
                    publish(pub, f'{room_id}.f2b', f2b)
