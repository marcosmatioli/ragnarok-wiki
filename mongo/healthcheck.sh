#!/bin/bash

mongo_url="mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@localhost:27017/"
status=$(mongosh --eval 'db.serverStatus().ok' ${mongo_url} --quiet)

if [ "$status" = "1" ]; then
    echo '{ "healthy": true }'
    exit 0
else
    echo "{ "healthy": false }"
    exit 1
fi
