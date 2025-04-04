#!/bin/bash

echo "Reorganizing AIseed Workspace..."

# Fix ownership and permissions
echo "Fixing ownership and permissions..."
sudo chown -R pong:pong /home/pong/Desktop/AIseed
find /home/pong/Desktop/AIseed -type d -exec chmod 755 {} \;  # Directories: rwxr-xr-x
find /home/pong/Desktop/AIseed -type f -exec chmod 644 {} \;  # Files: rw-r--r--

# Create directories if they don't exist
echo "Creating directories..."
mkdir -p /home/pong/Desktop/AIseed/cli
mkdir -p /home/pong/Desktop/AIseed/logs
mkdir -p /home/pong/Desktop/AIseed/nexus_seed/services
mkdir -p /home/pong/Desktop/AIseed/nexus_seed/utils

# Move files to their appropriate locations
echo "Reorganizing files..."
mv /home/pong/Desktop/AIseed/nexus_monitor_cli.py /home/pong/Desktop/AIseed/cli/
mv /home/pong/Desktop/AIseed/logs/.gitkeep /home/pong/Desktop/AIseed/logs/
mv /home/pong/Desktop/AIseed/nexus_seed/services/core_team.py /home/pong/Desktop/AIseed/nexus_seed/services/
mv /home/pong/Desktop/AIseed/nexus_seed/services/main_brain.py /home/pong/Desktop/AIseed/nexus_seed/services/
mv /home/pong/Desktop/AIseed/nexus_seed/utils/event_bus.py /home/pong/Desktop/AIseed/nexus_seed/utils/
mv /home/pong/Desktop/AIseed/startup.sh /home/pong/Desktop/AIseed/
mv /home/pong/Desktop/AIseed/main.py /home/pong/Desktop/AIseed/

echo "Workspace reorganization complete."
