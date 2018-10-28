# -*- coding: utf-8 -*-

import flask
import os
import yaml


app = flask.Flask(__name__)

__dir__ = os.path.dirname(__file__)
try:
    with open(os.path.join(__dir__, 'config.yaml')) as config_file:
        app.config.update(yaml.safe_load(config_file))
except FileNotFoundError:
    print('config.yaml file not found, assuming local development setup')
    app.secret_key = 'fake'


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/greet/<name>')
def greet(name):
    return flask.render_template('greet.html',
                                 name=name)

@app.route('/praise')
def praise():
    name = None
    praise = flask.session.get('praise', 'You rock!')

    return flask.render_template('praise.html',
                                 name=name,
                                 praise=praise)
