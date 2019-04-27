import os


if not {{ cookiecutter.set_up_pytest }}:
    os.remove('test_app.py')
