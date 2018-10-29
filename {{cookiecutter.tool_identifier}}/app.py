# -*- coding: utf-8 -*-

import flask
import mwapi
import mwoauth
import os
import random
import requests
import requests_oauthlib
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
    app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))

if 'oauth' in app.config:
    consumer_token = mwoauth.ConsumerToken(app.config['oauth']['consumer_key'], app.config['oauth']['consumer_secret'])


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

@app.template_global()
def authentication_area():
    if 'oauth' not in app.config:
        return flask.Markup()

    if 'oauth_access_token' not in flask.session:
        return (flask.Markup(r'<a id="login" class="navbar-text" href="') +
                flask.Markup.escape(flask.url_for('login')) +
                flask.Markup(r'">Log in</a>'))

    access_token = mwoauth.AccessToken(**flask.session['oauth_access_token'])
    identity = mwoauth.identify('https://www.wikidata.org/w/index.php',
                                consumer_token,
                                access_token)

    return (flask.Markup(r'<span class="navbar-text">Logged in as ') +
            user_link(identity['username']) +
            flask.Markup(r'</span>'))


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

    if 'oauth_access_token' in flask.session:
        access_token = mwoauth.AccessToken(**flask.session['oauth_access_token'])
        auth = requests_oauthlib.OAuth1(client_key=consumer_token.key, client_secret=consumer_token.secret,
                                        resource_owner_key=access_token.key, resource_owner_secret=access_token.secret)
        session = mwapi.Session(host='https://www.wikidata.org', auth=auth, user_agent=user_agent)

        userinfo = session.get(action='query', meta='userinfo', uiprop='options')['query']['userinfo']
        name = userinfo['name']
        gender = userinfo['options']['gender']
        if gender == 'male':
            default_praise = 'Praise him with great praise!'
        elif gender == 'female':
            default_praise = 'Praise her with great praise!'
        else:
            default_praise = 'Praise them with great praise!'
    else:
        name = None
        default_praise = 'You rock!'

    praise = flask.session.get('praise', default_praise)

    return flask.render_template('praise.html',
                                 name=name,
                                 praise=praise,
                                 csrf_error=csrf_error)

@app.route('/login')
def login():
    redirect, request_token = mwoauth.initiate('https://www.wikidata.org/w/index.php', consumer_token, user_agent=user_agent)
    flask.session['oauth_request_token'] = dict(zip(request_token._fields, request_token))
    return flask.redirect(redirect)

@app.route('/oauth/callback')
def oauth_callback():
    request_token = mwoauth.RequestToken(**flask.session['oauth_request_token'])
    access_token = mwoauth.complete('https://www.wikidata.org/w/index.php', consumer_token, request_token, flask.request.query_string, user_agent=user_agent)
    flask.session['oauth_access_token'] = dict(zip(access_token._fields, access_token))
    return flask.redirect(flask.url_for('index'))
