#!/bin/bash

python3.11 -m venv path/to/venv
source path/to/venv/bin/activate
python3.11 -m pip install --upgrade pip
pip3.11 install -r requirements.txt
python3.11 main.py
