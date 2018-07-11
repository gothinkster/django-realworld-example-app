#!/usr/bin/env bash
set -e  # fail fast

# bootstraps to django dev server from start to finish

CWD="$(cd "$(dirname "$0")" && pwd)"
pushd $CWD/..

DJANGO_PORT='4000'

function create_venv() {
    echo "Creating venv/ using system $(python3 --version) ..."
    python3 -m venv venv/ --clear

    echo "Upgrading packaging tools in venv..."
    venv/bin/pip install --upgrade --ignore-installed pip
    venv/bin/pip install --upgrade setuptools wheel
}

function install_app() {
    echo "Installing conduit from setup.py ..."
    venv/bin/pip install -e .
}

function migrate() {
    rm -rf *.sqlite3
    bin/django.sh migrate
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | bin/django.sh shell
}

function collectstatic() {
    bin/django.sh collectstatic --link --noinput
}

function runserver() {
    echo "Starting dev server, login to http://$(hostname -I | cut -d' ' -f1):${DJANGO_PORT} with admin@example.com/admin"
    bin/django.sh runserver 0.0.0.0:${DJANGO_PORT}
}

function main() {
    create_venv
    install_app
    migrate
#    collectstatic
    runserver
}

if [ $# -eq 0 ]; then
    main
elif [ $# -eq 1 ]; then
    "$@"  # call func by name ie. $ ./bootstrap.sh runserver
fi
