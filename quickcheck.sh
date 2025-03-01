#!/bin/bash
set -e

if [[ "$1" == "--install" ]]; then
  echo "Executando instalações via pip..."
  pip install pip-audit  # DEV
  pip install django-debug-toolbar  # DEV
  pip install flake8  # DEV
  pip install mypy  # DEV
  pip install types-beautifulsoup4
  pip install lxml-stubs
  pip install djangorestframework-stubs
  pip install types-python-dateutil
  pip install types-xmltodict
  pip install vulture
  pip install pylint
  pip install autopep8
  pip install pytest
  pip install coverage
fi

flake8 --max-line=100 --select=E,F,W,C --ignore=W503,W504,E731 apps adminlteui_custom config
mypy --install-types
#mypy apps *.py
#python -m pip_audit || true
coverage run manage.py test
coverage report -m
python -m pip_audit || true