.PHONY: check

check:{% if cookiecutter.set_up_flake8 == "True" %}
	flake8{% endif %}{% if cookiecutter.set_up_mypy == "True" %}
	MYPYPATH=stubs/ mypy .{% endif %}{% if cookiecutter.set_up_pytest == "True" %}
	pytest{% endif %}
