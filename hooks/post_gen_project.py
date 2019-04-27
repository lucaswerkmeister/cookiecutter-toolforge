import os


if not {{ cookiecutter.set_up_pytest }}:
    os.remove('test_app.py')

if not {{ cookiecutter.set_up_flake8 }} and \
   not {{ cookiecutter.set_up_mypy }} and \
   not {{ cookiecutter.set_up_pytest }}:
    os.remove('Makefile')
