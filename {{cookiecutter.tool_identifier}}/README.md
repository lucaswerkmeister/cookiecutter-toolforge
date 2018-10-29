# {{ cookiecutter.tool_name }}

[This tool](https://tools.wmflabs.org/{{ cookiecutter.tool_identifier }}/) does things.

For more information,
please see the tool’s [on-wiki documentation page](https://{{ cookiecutter.wiki_domain }}/wiki/User:{{ cookiecutter.user_name | replace(' ', '_') }}/{{ cookiecutter.tool_name | replace(' ', '_') }}).

## Toolforge setup

On Wikimedia Toolforge, this tool runs under the `{{ cookiecutter.tool_identifier }}` tool name.
Source code resides in `~/www/python/src/`,
a virtual environment is set up in `~/www/python/venv/`,
logs end up in `~/uwsgi.log`.

If the web service is not running for some reason, run the following command:
```
webservice --backend=kubernetes python start
```
If it’s acting up, try the same command with `restart` instead of `start`.

To update the service, run the following commands after becoming the tool account:
```
source ~/www/python/venv/bin/activate
cd ~/www/python/src
git fetch
git diff @ @{u} # inspect changes
git merge --ff-only @{u}
pip3 install -r requirements.txt
webservice --backend=kubernetes python restart
```

## Local development setup

You can also run the tool locally, which is much more convenient for development
(for example, Flask will automatically reload the application any time you save a file).

```
git clone https://phabricator.wikimedia.org/source/tool-{{ cookiecutter.tool_identifier }}.git
cd tool-{{ cookiecutter.tool_identifier }}
pip3 install -r requirements.txt
FLASK_APP=app.py FLASK_ENV=development flask run
```

If you want, you can do this inside some virtualenv too.

## License

The code in this repository is released under the AGPL v3, as provided in the `LICENSE` file.
