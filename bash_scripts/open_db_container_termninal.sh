#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

export $(grep -v '^#' .env | xargs)

docker exec -it worldnews-pipeline-news-postgres-1 psql -U $POSTGRES_USER -d $POSTGRES_DB