#!/bin/bash
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Full Restart of  System"

echo "Nuking everything..."
bash bash_scripts/nuke.sh
echo " "
echo " "
echo "========================="

echo "Initializing Airflow..."
bash bash_scripts/init_airflow.sh
echo " "
echo " "
echo "========================="

echo "Starting services..."
bash bash_scripts/start.sh
echo " "
echo " "
echo "========================="


echo "Done"