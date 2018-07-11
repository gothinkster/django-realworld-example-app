#!/usr/bin/env bash
set -e  # fail fast

CWD="$(cd "$(dirname "$0")" && pwd)"
pushd $CWD/..

venv/bin/python manage.py $1 ${@:2}
