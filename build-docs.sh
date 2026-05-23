#!/bin/bash
# This script is used to build the documentation (for the vercel hosted website)
# Thus I didn't bother setting up stuff like venv here ;)

# Switch to the directory of this file
cd "$( dirname "${BASH_SOURCE[0]}" )" || exit

# Even Vercel needs venvs now, since otherwise pip will not work
if [[ ! -f venv/bin/activate ]]; then
    echo "[*] Creating venv"
    python3 -m venv venv
fi
echo "[*] Using venv"
source venv/bin/activate

# install the dependencies
python3 -m pip install -r requirements.txt

if [[ -n "$DEPLOY_STABLE" ]]; then
    echo "[*] Downloading latest released version of this plugin"
    python3 -m pip install --force-reinstall --no-deps --upgrade mkdocs-badges
else
    echo "[*] Installing bleading edge version of this plugin"
    python3 -m pip install .
fi

# Vercel prefers outputs to be in public/
python3 -m properdocs build -d public

if [[ -n "$1" ]]; then
    echo "[*] Starting web server on 127.0.0.1:$1"
    python3 -m http.server --bind 127.0.0.1 --directory public "$1"
fi