#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Starting all services..."
docker compose up airflow-webserver airflow-scheduler news-postgres -d

echo "Waiting for services to be ready..."
sleep 10

echo "Checking containers..."
docker ps

echo ""
echo "Airflow UI: http://localhost:8080"
echo "Login: admin / admin"