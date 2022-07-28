#!/usr/bin/env bash

pwd

docker-compose -f integration_test/docker-compose.yaml up  -d

sleep 20

aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration

echo 'successfully created the target'

pipenv run python integration_test/tests/integration_test.py

pipenv run pytest  tests/test_batch.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose -f integration_test/docker-compose.yaml logs
    docker-compose -f integration_test/docker-compose.yaml down -d
    exit ${ERROR_CODE}
fi





docker-compose -f integration_test/docker-compose.yaml down -d