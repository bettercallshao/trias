# -*- coding: utf-8 -*-
"""Tests for msgque module."""


from time import sleep

import trias.game.trivia as trivia
from trias.database.table import Script


def test_happy_path():
    def get_script():
        return Script(
            title='chen',
            question='1+1=?',
            optiona='35',
            optionb='jesus',
            optionc='DOS',
            answer='c',
        )

    game = trivia.Trivia(get_script)

    # Empty
    assert game.tick(None) is None
    sleep(1)

    # Waiting
    accept = game.tick(None)
    assert accept['type'] == trivia.ACCEPT

    def add_player():
        game.tick({
            'type': trivia.JOIN,
            'session_id': accept['session_id']
        })

    for _ in range(3):
        add_player()

    assert game.start_count == 3

    for _ in range(7):
        add_player()

    # Asking
    question = game.tick(None)
    assert question['type'] == trivia.QUESTION
    assert question['title'] == 'chen'
    assert question['index'] == 0

    # Listening
    def pick_option(option):
        game.tick({
            'type': trivia.ANSWER,
            'answer': option,
            'session_id': question['session_id'],
            'round_id': question['round_id'],
        })

    pick_option('a')
    pick_option('b')
    pick_option('c')
    pick_option('c')
    pick_option('c')

    sleep(10)

    # Counting
    correct = game.tick(None)
    assert correct['type'] == trivia.CORRECT
    assert correct['count_a'] == 1
    assert correct['count_b'] == 1
    assert correct['count_c'] == 3

    # Next round
    second = game.tick(None)
    assert second['index'] == 1
    sleep(10)

    # Next game
    game.tick(None)
    assert game.session_state == trivia.EMPTY
