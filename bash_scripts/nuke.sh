#!/bin/bash
echo "Stopping and removing all containers..."
docker compose down -v --remove-orphans

echo "Removing built images..."
docker rmi worldnews-pipeline-airflow-webserver 2>/dev/null
docker rmi worldnews-pipeline-airflow-scheduler 2>/dev/null
docker rmi worldnews-pipeline-airflow-init 2>/dev/null

echo "Cleaning logs..."
rm -rf ../logs/*

echo "Done. Everything removed."