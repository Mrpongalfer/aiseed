#!/bin/bash

echo "Starting AIseed Workspace..."

# Suppress TensorFlow warnings
export TF_CPP_MIN_LOG_LEVEL=2

# Suppress specific FutureWarnings
export PYTHONWARNINGS="ignore::FutureWarning"

# Set PYTHONPATH to include the project root
export PYTHONPATH=/home/pong/Desktop/AIseed

# Load PostgreSQL credentials from .env
source /home/pong/Desktop/AIseed/.env

# Check if the virtual environment exists
if [ ! -d "/home/pong/Desktop/AIseed/.venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv /home/pong/Desktop/AIseed/.venv
    source /home/pong/Desktop/AIseed/.venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r /home/pong/Desktop/AIseed/requirements.txt
else
    source /home/pong/Desktop/AIseed/.venv/bin/activate
fi

# Verify dependencies
echo "Verifying dependencies..."
pip check || echo "Some dependencies may have conflicts. Please review."

# Ensure PostgreSQL is running
echo "Ensuring PostgreSQL is running..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Ensure Docker is running
echo "Ensuring Docker is running..."
sudo systemctl start docker
sudo systemctl enable docker

# Unset invalid DOCKER_HOST if set
if [ "$DOCKER_HOST" == "http+docker://" ]; then
    echo "Unsetting invalid DOCKER_HOST..."
    unset DOCKER_HOST
fi

# Ensure Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Installing..."
    sudo apt update
    sudo apt install -y docker-compose
fi

# Ensure Docker Compose services are running
echo "Starting Docker Compose services..."
docker-compose -f /home/pong/Desktop/AIseed/docker-compose.yml up -d

# Wait for services to be ready
echo "Waiting for services to initialize..."
sleep 10

# Start the system
echo "Starting AIseed system..."
python /home/pong/Desktop/AIseed/main.py
