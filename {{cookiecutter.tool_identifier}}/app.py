# -*- coding: utf-8 -*-

import flask


app = flask.Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'
