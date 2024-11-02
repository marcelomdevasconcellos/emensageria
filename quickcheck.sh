#!/bin/bash

clear
set -e
flake8 --max-line=100 --select=E,F,W,C --ignore=W503,W504,E731 apps
mypy --install-types
mypy apps *.py
python -m pip_audit || true