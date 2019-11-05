#!/usr/bin/env bash

#
# This script presumes that you have PostgreSQL setup and running
# If you need GIS support you'll need a one time server setup
# Please take a look at https://github.com/wooyek/docker-geodjango/blob/master/docker-entrypoint.sh
#

ENV=$(dirname $(dirname $(readlink -fm $0)))/.env
echo "------> Loading env ${ENV}"
while read -r line; do declare -x "$line"; done < <(cat $ENV | egrep -v "(^#|^\s|^$)")

echo "------> Dropping database ${DATABASE_NAME}"
sudo -u postgres -E sh -c 'dropdb ${DATABASE_NAME}'

echo "------> Dropping database ${DATABASE_TEST_NAME}"
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw0'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw1'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw2'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw3'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw4'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw5'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw6'
sudo -u postgres -E sh -c 'dropdb ${DATABASE_TEST_NAME}_gw7'

echo "------> Creating database ${DATABASE_NAME}"
sudo -u postgres -E sh -c 'createdb ${DATABASE_NAME}'

echo "------> Creating database ${DATABASE_TEST_NAME}"
sudo -u postgres -E sh -c 'createdb ${DATABASE_TEST_NAME}'


echo "[ OK ] ${BASH_SOURCE[0]}"



