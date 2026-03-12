#!/bin/bash
docker exec -it worldnews-postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}