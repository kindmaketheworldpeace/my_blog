#!/usr/bin/env bash

python manage.py celery worker --settings=settings -l info -c 1