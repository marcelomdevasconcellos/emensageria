#!/bin/bash

#pip install pip-audit  # DEV
#pip install django-debug-toolbar  # DEV
#pip install flake8  # DEV
#pip install mypy  # DEV
#pip install types-beautifulsoup4
#pip install lxml-stubs
#pip install djangorestframework-stubs
#pip install types-python-dateutil
#pip install types-xmltodict
#pip install vulture
#pip install pylint
#pip install autopep8

set -e
flake8 --max-line=100 --select=E,F,W,C --ignore=W503,W504,E731 apps adminlteui_custom config
mypy --install-types
mypy apps *.py
python -m pip_audit || true