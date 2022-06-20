#!/bin/bash

#kill all tmux sessions
tmux kill-server

cd ./flask-portfolio

#updates project
git fetch && git reset origin/main --hard

#enters virtual environment and installs dependencies
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

#deploys website
tmux new -d -s site-session 'flask run --host=0.0.0.0'
tmux send-keys 'exec redeploy-site.sh' C-m
tmux detach -s site-session
