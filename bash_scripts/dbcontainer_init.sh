#!/bin/bash
docker run -d \
  --name news-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=newsdb \
  -p 5432:5432 \
  postgres:15

docker ps