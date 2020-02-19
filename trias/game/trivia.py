# -*- coding: utf-8 -*-
"""Game logic.

message types:

backend -> frontend:
    accept
    question
    correct

frontend -> backend:
    join
    answer


"""

from uuid import uuid4
from datetime import datetime

EMPTY = 'EMPTY'
WAITING = 'WAITING'
PLAYING = 'PLAYING'

TO_ASK = 'TO_ASK'
LISTENING = 'LISTENING'
COUNTING = 'COUNTING'

ACCEPT = 'ACCEPT'
QUESTION = 'QUESTION'
CORRECT = 'CORRECT'

JOIN = 'JOIN'
ANSWER = 'ANSWER'


class Trivia(object):

    def __init__(self, get_script):
        self.get_script = get_script

        self.session_state = EMPTY
        self.session_id = ''
        self.start_count = 0
        self.round_index = 0

        self.round_state = EMPTY
        self.round_id = ''
        self.round_count = None
        self.script = None

        self.last_action = None

    def since_action(self):
        return (datetime.now() - self.last_action).total_seconds()

    def stamp_action(self):
        self.last_action = datetime.now()

    def validate_session(self, msg):
        return msg and 'session_id' in msg and msg['session_id'] == self.session_id

    def validate_round(self, msg):
        return msg and 'round_id' in msg and msg['round_id'] == self.round_id

    def tick(self, msg):
        """Process a incoming message or a timed tick"""
        if self.last_action is None:
            self.stamp_action()

        # Empty state simply advances to waiting
        if self.session_state == EMPTY:
            self.session_id = str(uuid4())
            self.session_state = WAITING
            self.start_count = 0

        # Waiting state broadcasts and accepts joins
        elif self.session_state == WAITING:

            # Count new joins
            if self.validate_session(msg):
                if msg['type'] == JOIN:
                    self.start_count += 1

            # State change
            if self.start_count >= 10:
                self.session_state = PLAYING
                self.round_index = 0
                self.round_state = TO_ASK

            # Broadcast we are accepting
            if self.since_action() > 1:
                self.stamp_action()
                return {
                    'type': ACCEPT,
                    'session_id': self.session_id,
                }

        # Game in progress
        elif self.session_state == PLAYING:
            if self.round_state == TO_ASK:
                self.round_id = str(uuid4())
                self.round_count = {
                    'a': 0,
                    'b': 0,
                    'c': 0,
                }
                self.script = self.get_script()
                self.round_state = LISTENING
                self.stamp_action()
                return {
                    'type': QUESTION,
                    'title': self.script.title,
                    'question': self.script.question,
                    'option_a': self.script.optiona,
                    'option_b': self.script.optionb,
                    'option_c': self.script.optionc,
                    'index': self.round_index,
                    'session_id': self.session_id,
                    'round_id': self.round_id,
                }

            if self.round_state == LISTENING:
                if self.since_action() > 10:
                    self.round_state = COUNTING

                if self.validate_session(msg) and self.validate_round(msg):
                    if msg['type'] == ANSWER:
                        self.round_count[msg['answer']] += 1

            if self.round_state == COUNTING:
                # Is game over?
                over = self.round_count[self.script.answer] <= 1

                self.round_index += 1
                self.round_state = TO_ASK

                if over:
                    self.session_state = EMPTY

                return {
                    'type': CORRECT,
                    'answer': self.script.answer,
                    'count_a': self.round_count['a'],
                    'count_b': self.round_count['b'],
                    'count_c': self.round_count['c'],
                    'index': self.round_index,
                    'over': over,
                    'session_id': self.session_id,
                    'round_id': self.round_id,
                }
