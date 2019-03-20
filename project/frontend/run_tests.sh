#!/bin/bash


python3 manage.py test tests.login

python3 manage.py test tests.bad_login

python3 manage.py test tests.api_backend

python3 manage.py test tests.dashboard

#python3 manage.py test tests.performance

