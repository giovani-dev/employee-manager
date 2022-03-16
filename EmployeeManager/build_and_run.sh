#!/usr/bin/env bash
python EmployeeManager/manage.py makemigrations
python EmployeeManager/manage.py makemigrations employee
python EmployeeManager/manage.py migrate
(cd EmployeeManager; gunicorn EmployeeManager.wsgi --user www-data --bind 0.0.0.0:8000 --workers 2)