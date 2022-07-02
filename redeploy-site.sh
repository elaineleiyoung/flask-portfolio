#!/bin/bash

cd ./flask-portfolio

#updates project
git fetch && git reset origin/main --hard

#enters virtual environment and installs dependencies
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

#deploys website by restarting myportfolio service
systemctl daemon-reload
systemctl restart myportfolio
