#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Creating required directories..."
mkdir -p logs plugins

echo "Initializing Airflow..."
docker compose up airflow-init --exit-code-from airflow-init

echo "Airflow initialized."