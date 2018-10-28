# -*- coding: utf-8 -*-

import flask
import os
import random
import string
import yaml


app = flask.Flask(__name__)

__dir__ = os.path.dirname(__file__)
try:
    with open(os.path.join(__dir__, 'config.yaml')) as config_file:
        app.config.update(yaml.safe_load(config_file))
except FileNotFoundError:
    print('config.yaml file not found, assuming local development setup')
    app.secret_key = 'fake'


@app.template_global()
def csrf_token():
    if 'csrf_token' not in flask.session:
        flask.session['csrf_token'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
    return flask.session['csrf_token']


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/greet/<name>')
def greet(name):
    return flask.render_template('greet.html',
                                 name=name)

@app.route('/praise', methods=['GET', 'POST'])
def praise():
    if flask.request.method == 'POST':
        token = flask.session.pop('csrf_token', None)
        if token and token == flask.request.form.get('csrf_token'):
            flask.session['praise'] = flask.request.form.get('praise', 'praise missing')

    name = None
    praise = flask.session.get('praise', 'You rock!')

    return flask.render_template('praise.html',
                                 name=name,
                                 praise=praise)
