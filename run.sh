#!/bin/bash

export DB_HOST=015cacf79e48
export DB_USER=postgres
export DB_PASS=1234
export DB_SCHEME=sa

export API_BASE_URL=http://back:8001

docker-compose up -d --force-recreate
