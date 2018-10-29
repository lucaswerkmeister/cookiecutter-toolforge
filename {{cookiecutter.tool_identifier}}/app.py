# -*- coding: utf-8 -*-

import flask
import os
import random
import requests
import string
import toolforge
import yaml


app = flask.Flask(__name__)

app.before_request(toolforge.redirect_to_https)

toolforge.set_user_agent('{{ cookiecutter.tool_identifier }}', email='{{ cookiecutter.user_email }}')
user_agent = requests.utils.default_user_agent()

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

@app.template_global()
def form_value(name):
    if 'repeat_form' in flask.g and name in flask.request.form:
        return (flask.Markup(r' value="') +
                flask.Markup.escape(flask.request.form[name]) +
                flask.Markup(r'" '))
    else:
        return flask.Markup()

@app.template_global()
def form_attributes(name):
    return (flask.Markup(r' id="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" name="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" ') +
            form_value(name))

@app.template_filter()
def user_link(user_name):
    return (flask.Markup(r'<a href="https://www.wikidata.org/wiki/User:') +
            flask.Markup.escape(user_name.replace(' ', '_')) +
            flask.Markup(r'">') +
            flask.Markup(r'<bdi>') +
            flask.Markup.escape(user_name) +
            flask.Markup(r'</bdi>') +
            flask.Markup(r'</a>'))


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/greet/<name>')
def greet(name):
    return flask.render_template('greet.html',
                                 name=name)

@app.route('/praise', methods=['GET', 'POST'])
def praise():
    csrf_error = False
    if flask.request.method == 'POST':
        token = flask.session.pop('csrf_token', None)
        if token and token == flask.request.form.get('csrf_token'):
            flask.session['praise'] = flask.request.form.get('praise', 'praise missing')
        else:
            csrf_error = True
            flask.g.repeat_form = True

    name = None
    praise = flask.session.get('praise', 'You rock!')

    return flask.render_template('praise.html',
                                 name=name,
                                 praise=praise,
                                 csrf_error=csrf_error)
