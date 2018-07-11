#!/usr/bin/env bash
# Use this script to regenerate requirements.txt from packages installed in venv/ using pipdeptree's nice tree layout

CWD="$(cd "$(dirname "$0")" && pwd)"
pushd $CWD/..

echo "Generating new requirements.txt ..."
venv/bin/pipdeptree --local-only --freeze --exclude pip,setuptools,wheel,conduit > requirements.txt

popd
