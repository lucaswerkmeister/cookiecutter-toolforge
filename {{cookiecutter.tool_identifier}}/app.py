# -*- coding: utf-8 -*-

import flask


app = flask.Flask(__name__)


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
