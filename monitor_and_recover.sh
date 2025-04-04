#!/bin/bash

echo "Monitoring AIseed system..."

while true; do
    # Check if the main process is running
    if ! pgrep -f "python /home/aiseed/AIseed/main.py" > /dev/null; then
        echo "Main process is not running. Attempting to restart..."
        ssh aiseed@192.168.0.95 "bash /home/aiseed/AIseed/startup.sh"
    else
        echo "Main process is running."
    fi
    sleep 10
done
