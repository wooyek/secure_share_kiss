#!/usr/bin/env bash
echo "============================================="
echo "Docker image for django web project"
echo "============================================="

echo "------> Please note tooling versions"
which python
python -V
python3 -V
easy_install --version
pip --version
tox --version
git --version
echo "------> Checking venv"
virtualenv --version
python3 -m venv -h
echo "------> Python 2 packages"
pip2 freeze
echo "------> Python 3 packages"
pip3 freeze

echo "------> manage.py collectstatic"
python3 /app/manage.py collectstatic --noinput

echo "------> manage.py migrate"
python3 /app/manage.py migrate

# echo "------> Staring up gunicorn..."
# gunicorn --chdir=/app/src secure_share_kiss.wsgi:application --timeout 240 --graceful-timeout 230 --log-file -

echo "------> Staring up django runserver..."
python3 /app/manage.py migrate

echo "------> Creating superuser if no users exits"
python3 /app/bin/superuser.py

echo "------> Running command passed down do container..."
exec "$@"
