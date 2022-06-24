# cookiecutter-toolforge

A [cookiecutter](https://github.com/audreyr/cookiecutter) template
for Wikimedia Toolforge tools using the Flask Python framework.

## Usage

[Install `cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/installation.html) if it’s not already installed on your system.
On a Linux system, the following command should work:

```sh
sudo pip install cookiecutter
```

Once `cookiecutter` is installed, you can create a new tool project with the following command:

```sh
cookiecutter gh:lucaswerkmeister/cookiecutter-toolforge
```

You will be prompted for some metadata about the tool (see [below](#Variables) for details),
and then the resulting source code will be placed into a directory named after the tool’s identifier
(the first thing you were asked for).
Change into that directory, install dependencies and run the tool locally:

```sh
cd <tool_identifier>
pip install -r requirements.txt
FLASK_ENV=development FLASK_APP=app.py flask run
```

Then, open http://localhost:5000/ and follow the further instructions there.

### Variables

You will be prompted for the following variables:

* **tool_identifier**: The identifier of the tool, which will be used in the URL.
  Usually only uses letters and hyphens, sometimes also digits or underscores.
* **tool_name**: The name of the tool. This can be any text.
* **user_name**: Your user name on Wikimedia wikis.
  This is mainly used to generate the link to the tool’s documentation:
  by default, the link will point to a subpage of your user page.
  (You can change this, of course.)
* **wiki_domain**: The domain name of the main wiki the tool will target.
  This is used for the documentation link and also for OAuth.
  If your tool targets several wikis, you can use `meta.wikimedia.org`.
* **set_up_flake8**: Whether to set up [Flake8](https://flake8.pycqa.org/), a Python code style checker.
  Enable this if you want to use Flake8 to ensure a consistent code style (e.g. indentation or spacing).
  Flake8 can also catch some programming mistakes, such as unused variables or imports.
* **set_up_mypy**: Whether to set up [mypy](http://mypy-lang.org/), a Python static type checker.
  Enable this if you want to annotate your code with static types and use mypy to check them.
  mypy can catch more mistakes than Flake8, but can also be harder to work with;
  it’s more useful for more complicated tools with larger codebases.
* **set_up_pytest**: Whether to set up [pytest](https://docs.pytest.org/), a Python testing framework.
  Enable this if you want to write tests for your tool and run them with pytest.
  Automated tests are very useful to ensure that your tool keeps working when the code is changed later.
* **set_up_github_ci**: Whether to set up Continuous Integration using [GitHub Actions](https://github.com/features/actions).
  Enable this if you plan to publish your tool’s code on GitHub and want to automatically run the checks configured with the previous variables.

## Features

The full list of features is on the tool’s default index page once you follow the instructions above,
but in brief, this template includes:

* A basic HTML template, using Bootstrap v4.0.
* Examples of Flask routing and templating.
* Form handling, including CSRF protection.
* Authentication against Wikimedia sites using OAuth.
* Optionally, automated code style (Flake8), type (mypy) and functionality (pytest) checks.

![screenshot](https://raw.githubusercontent.com/lucaswerkmeister/cookiecutter-toolforge/master/screenshot.png)

## License

This template is released under the MIT license, as provided in the `LICENSE` file that accompanies it.
By contributing to the repository, you agree to license your contribution under this license.

Generated projects (tools) use the GNU AGPL v3 by default,
but you are free to choose any license you want,
and no formal attribution to this template is required
(though some form of attribution is still appreciated).
In terms of the license,
projects are not considered “substantial portions of the Software” (i. e. the template).
