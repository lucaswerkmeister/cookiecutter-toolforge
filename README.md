# cookiecutter-toolforge

A [cookiecutter](https://github.com/audreyr/cookiecutter) template
for Wikimedia Toolforge tools using the Flask Python framework.

## Usage

Install `cookiecutter` if it’s not already installed on your system.
If it’s not available in your package manager, the following command should work:

```sh
sudo pip install cookiecutter
```

Once `cookiecutter` is installed, you can create a new tool project with the following command:

```sh
cookiecutter gh:lucaswerkmeister/cookiecutter-toolforge
```

You will be prompted for some metadata about the tool,
and then the resulting source code will be placed into a directory named after the tool’s identifier
(the first thing you were asked for).
Change into that directory and run the tool locally:

```sh
cd <tool_identifier>
FLASK_ENV=development FLASK_APP=app.py flask run
```

Then, open http://localhost:5000/ and follow the further instructions there.

## Features

The full list of features is on the tool’s default index page once you follow the instructions above,
but in brief, this template includes:

* A basic HTML template, using Bootstrap v4.0.
* Examples of Flask routing and templating.
* Form handling, including CSRF protection.
* Authentication against Wikimedia sites using OAuth.

## License

This template is released under the MIT license, as provided in the `LICENSE` file that accompanies it.
By contributing to the repository, you agree to license your contribution under this license.

Generated projects (tools) use the GNU AGPL v3 by default,
but you are free to choose any license you want,
and no formal attribution to this template is required
(though some form of attribution is still appreciated).
In terms of the license,
projects are not considered “substantial portions of the Software” (i. e. the template).
