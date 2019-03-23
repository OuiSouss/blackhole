#!/bin/sh
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_PORT=5555
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
flask run --port=$FLASK_PORT