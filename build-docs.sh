#!/bin/bash
# This script is used to build the documentation (for the vercel hosted website)
# Thus I didn't bother setting up stuff like venv here ;)

# Switch to the directory of this file
cd "$( dirname "${BASH_SOURCE[0]}" )" || exit

# install the dependencies
python3 -m pip install poetry
python3 -m poetry install

if [[ -n "$DEPLOY_STABLE" ]]; then
    echo "[*] Downloading latest released version of this plugin"
    python3 -m poetry run pip install --force-reinstall --no-deps --upgrade mkdocs-badges
fi

# Vercel prefers outputs to be in public/
poetry run mkdocs build -d public

if [[ -n "$1" ]]; then
    echo "[*] Starting web server on 127.0.0.1:$1"
    python3 -m http.server --bind 127.0.0.1 --directory public "$1"
fi