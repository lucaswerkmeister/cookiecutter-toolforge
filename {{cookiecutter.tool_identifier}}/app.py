# -*- coding: utf-8 -*-

import flask
import mwapi{% if cookiecutter.set_up_mypy == "True" %}  # type: ignore{% endif %}
import mwoauth{% if cookiecutter.set_up_mypy == "True" %}  # type: ignore{% endif %}
import os
import random
import requests_oauthlib{% if cookiecutter.set_up_mypy == "True" %}  # type: ignore{% endif %}
import string
import toolforge
{% if cookiecutter.set_up_mypy == "True" %}from typing import Optional, Tuple
import werkzeug
{% endif %}import yaml


app = flask.Flask(__name__)

user_agent = toolforge.set_user_agent(
    '{{ cookiecutter.tool_identifier }}',
    email='{{ cookiecutter.user_email }}')

__dir__ = os.path.dirname(__file__)
try:
    with open(os.path.join(__dir__, 'config.yaml')) as config_file:
        app.config.update(yaml.safe_load(config_file))
except FileNotFoundError:
    print('config.yaml file not found, assuming local development setup')
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(64))
    app.secret_key = random_string

if 'oauth' in app.config:
    oauth_config = app.config['oauth']
    consumer_token = mwoauth.ConsumerToken(oauth_config['consumer_key'],
                                           oauth_config['consumer_secret'])
    index_php = 'https://{{ cookiecutter.wiki_domain }}/w/index.php'


@app.template_global()
def csrf_token(){% if cookiecutter.set_up_mypy == "True" %} -> str{% endif %}:
    if 'csrf_token' not in flask.session:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(64))
        flask.session['csrf_token'] = random_string
    return flask.session['csrf_token']


@app.template_global()
def form_value(name{% if cookiecutter.set_up_mypy == "True" %}: str{% endif %}){% if cookiecutter.set_up_mypy == "True" %} -> flask.Markup{% endif %}:
    if 'repeat_form' in flask.g and name in flask.request.form:
        return (flask.Markup(r' value="') +
                flask.Markup.escape(flask.request.form[name]) +
                flask.Markup(r'" '))
    else:
        return flask.Markup()


@app.template_global()
def form_attributes(name{% if cookiecutter.set_up_mypy == "True" %}: str{% endif %}){% if cookiecutter.set_up_mypy == "True" %} -> flask.Markup{% endif %}:
    return (flask.Markup(r' id="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" name="') +
            flask.Markup.escape(name) +
            flask.Markup(r'" ') +
            form_value(name))


@app.template_filter()
def user_link(user_name{% if cookiecutter.set_up_mypy == "True" %}: str{% endif %}){% if cookiecutter.set_up_mypy == "True" %} -> flask.Markup{% endif %}:
    user_href = 'https://{{ cookiecutter.wiki_domain }}/wiki/User:'
    return (flask.Markup(r'<a href="' + user_href) +
            flask.Markup.escape(user_name.replace(' ', '_')) +
            flask.Markup(r'">') +
            flask.Markup(r'<bdi>') +
            flask.Markup.escape(user_name) +
            flask.Markup(r'</bdi>') +
            flask.Markup(r'</a>'))


@app.template_global()
def authentication_area(){% if cookiecutter.set_up_mypy == "True" %} -> flask.Markup{% endif %}:
    if 'oauth' not in app.config:
        return flask.Markup()

    if 'oauth_access_token' not in flask.session:
        return (flask.Markup(r'<a id="login" class="navbar-text" href="') +
                flask.Markup.escape(flask.url_for('login')) +
                flask.Markup(r'">Log in</a>'))

    access_token = mwoauth.AccessToken(**flask.session['oauth_access_token'])
    identity = mwoauth.identify(index_php,
                                consumer_token,
                                access_token)

    return (flask.Markup(r'<span class="navbar-text">Logged in as ') +
            user_link(identity['username']) +
            flask.Markup(r'</span>'))


def authenticated_session(){% if cookiecutter.set_up_mypy == "True" %} -> Optional[mwapi.Session]{% endif %}:
    if 'oauth_access_token' not in flask.session:
        return None

    access_token = mwoauth.AccessToken(
        **flask.session['oauth_access_token'])
    auth = requests_oauthlib.OAuth1(client_key=consumer_token.key,
                                    client_secret=consumer_token.secret,
                                    resource_owner_key=access_token.key,
                                    resource_owner_secret=access_token.secret)
    return mwapi.Session(host='https://{{ cookiecutter.wiki_domain }}',
                         auth=auth,
                         user_agent=user_agent)


@app.route('/')
def index(){% if cookiecutter.set_up_mypy == "True" %} -> str{% endif %}:
    return flask.render_template('index.html')


@app.route('/greet/<name>')
def greet(name{% if cookiecutter.set_up_mypy == "True" %}: str{% endif %}){% if cookiecutter.set_up_mypy == "True" %} -> str{% endif %}:
    return flask.render_template('greet.html',
                                 name=name)


@app.route('/praise', methods=['GET', 'POST'])
def praise(){% if cookiecutter.set_up_mypy == "True" %} -> str{% endif %}:
    csrf_error = False
    if flask.request.method == 'POST':
        if submitted_request_valid():
            praise = flask.request.form.get('praise', 'praise missing')
            flask.session['praise'] = praise
        else:
            csrf_error = True
            flask.g.repeat_form = True

    session = authenticated_session()
    if session:
        userinfo = session.get(action='query',
                               meta='userinfo',
                               uiprop='options')['query']['userinfo']
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
def login(){% if cookiecutter.set_up_mypy == "True" %} -> werkzeug.Response{% endif %}:
    redirect, request_token = mwoauth.initiate(index_php,
                                               consumer_token,
                                               user_agent=user_agent)
    flask.session['oauth_request_token'] = dict(zip(request_token._fields,
                                                    request_token))
    return flask.redirect(redirect)


@app.route('/oauth/callback')
def oauth_callback(){% if cookiecutter.set_up_mypy == "True" %} -> werkzeug.Response{% endif %}:
    request_token = mwoauth.RequestToken(
        **flask.session.pop('oauth_request_token'))
    access_token = mwoauth.complete(index_php,
                                    consumer_token,
                                    request_token,
                                    flask.request.query_string,
                                    user_agent=user_agent)
    flask.session['oauth_access_token'] = dict(zip(access_token._fields,
                                                   access_token))
    return flask.redirect(flask.url_for('index'))


def full_url(endpoint{% if cookiecutter.set_up_mypy == "True" %}: str{% endif %}, **kwargs){% if cookiecutter.set_up_mypy == "True" %} -> str{% endif %}:
    scheme = flask.request.headers.get('X-Forwarded-Proto', 'http')
    return flask.url_for(endpoint, _external=True, _scheme=scheme, **kwargs)


def submitted_request_valid(){% if cookiecutter.set_up_mypy == "True" %} -> bool{% endif %}:
    """Check whether a submitted POST request is valid.

    If this method returns False, the request might have been issued
    by an attacker as part of a Cross-Site Request Forgery attack;
    callers MUST NOT process the request in that case.
    """
    real_token = flask.session.pop('csrf_token', None)
    submitted_token = flask.request.form.get('csrf_token', None)
    if not real_token:
        # we never expected a POST
        return False
    if not submitted_token:
        # token got lost or attacker did not supply it
        return False
    if submitted_token != real_token:
        # incorrect token (could be outdated or incorrectly forged)
        return False
    return True


# If you don’t want to handle CSRF protection in every POST handler,
# you can instead uncomment the @app.before_request decorator
# on the following function,
# which will raise a very generic error for any invalid POST.
# Otherwise, you can remove the whole function.
# @app.before_request
def require_valid_submitted_request(){% if cookiecutter.set_up_mypy == "True" %} -> Optional[Tuple[str, int]]{% endif %}:
    if flask.request.method == 'POST' and not submitted_request_valid():
        return 'CSRF error', 400  # stop request handling
    return None  # continue request handling


@app.after_request
def deny_frame(response{% if cookiecutter.set_up_mypy == "True" %}: flask.Response{% endif %}){% if cookiecutter.set_up_mypy == "True" %} -> flask.Response{% endif %}:
    """Disallow embedding the tool’s pages in other websites.

    Not every tool can be usefully embedded in other websites, but
    allowing embedding can expose the tool to clickjacking
    vulnerabilities, so err on the side of caution and disallow
    embedding. This can be removed (possibly only for certain pages)
    as long as other precautions against clickjacking are taken.
    """
    response.headers['X-Frame-Options'] = 'deny'
    return response
