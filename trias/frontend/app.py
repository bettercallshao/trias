# -*- coding: utf-8 -*-
"""Flask app layer."""

import os

from flask import Flask, render_template

app = Flask('trias', root_path=os.path.dirname(__file__))


@app.route('/')
def home():
    return render_template('home.html')
