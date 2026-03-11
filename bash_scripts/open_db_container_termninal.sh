#!/bin/bash
docker exec -it news-postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}