import os
import sys


if not {{ cookiecutter.set_up_mypy }}:
    os.remove('stubs/toolforge.pyi')
    os.rmdir('stubs')

if not {{ cookiecutter.set_up_pytest }}:
    os.remove('test_app.py')

if not {{ cookiecutter.set_up_github_ci }}:
    os.remove('.github/workflows/test.yaml')
    os.rmdir('.github/workflows')
    os.rmdir('.github')

if not {{ cookiecutter.set_up_flake8 }} and \
   not {{ cookiecutter.set_up_mypy }} and \
   not {{ cookiecutter.set_up_pytest }}:
    os.remove('Makefile')

    if {{ cookiecutter.set_up_github_ci }}:
        print('\033[1m', file=sys.stderr)  # ANSI SGR 1: bold text
        print('''

You specified that GitHub CI support should be enabled, but that
neither Flake8 nor mypy nor pytest should be set up. Since this leaves
us with no automatic checks, no Makefile has been created, and the
`make check` command configured in .github/workflows/test.yaml will
fail unless you create a custom Makefile with a `check` goal.

    '''.strip(), file=sys.stderr)
        print('\033[0m', file=sys.stderr)  # ANSI SGR 0: reset/normal
