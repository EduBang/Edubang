#!/bin/bash

clear
echo "EduBang"
cat data/command/edubang_ascii.txt

PYTHON_PATH=$(which python3 || which python)

if [ -z "$PYTHON_PATH" ]; then
    echo "Erreur : Python n'est pas installé."
    exit 1
fi

"$PYTHON_PATH" -m pip install -r requirements.txt

"$PYTHON_PATH" ./sources/main.py
