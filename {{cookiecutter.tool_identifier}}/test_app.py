import pytest{% if cookiecutter.set_up_mypy %}  # type: ignore{% endif %}
import re

{% set tool_identifier_python = cookiecutter.tool_identifier | replace('-', '_') %}import app as {{ tool_identifier_python }}


@pytest.fixture
def client():
    {{ tool_identifier_python }}.app.testing = True
    client = {{ tool_identifier_python }}.app.test_client()

    with client:
        yield client
    # request context stays alive until the fixture is closed


def test_csrf_token_generate():
    with {{ tool_identifier_python }}.app.test_request_context():
        token = {{ tool_identifier_python }}.csrf_token()
        assert token != ''


def test_csrf_token_save():
    with {{ tool_identifier_python }}.app.test_request_context() as context:
        token = {{ tool_identifier_python }}.csrf_token()
        assert token == context.session['csrf_token']


def test_csrf_token_load():
    with {{ tool_identifier_python }}.app.test_request_context() as context:
        context.session['csrf_token'] = 'test token'
        assert {{ tool_identifier_python }}.csrf_token() == 'test token'


def test_praise(client):
    # default praise
    response = client.get('/praise')
    html = response.get_data(as_text=True)
    assert '<h2>You rock!</h2>' in html

    # extract CSRF token
    match = re.search(r'name="csrf_token" type="hidden" value="([^"]*)"', html)
    assert match is not None
    csrf_token = match.group(1)

    referrer = {{ tool_identifier_python }}.full_url('praise')
    headers = {'Referer': referrer}

    # update praise
    response = client.post('/praise',
                           data={'csrf_token': csrf_token,
                                 'praise': 'How cool!'},
                           headers=headers)
    html = response.get_data(as_text=True)
    assert '<h2>How cool!</h2>' in html
    assert 'You rock!' not in html

    # try to update praise with wrong CSRF token
    response = client.post('/praise',
                           data={'csrf_token': 'wrong ' + csrf_token,
                                 'praise': 'Boo!'},
                           headers=headers)
    html = response.get_data(as_text=True)
    assert '<h2>Boo!</h2>' not in html
    assert '<h2>How cool!</h2>' in html
    assert 'value="Boo!"' in html  # input is repeated
