#!/bin/bash

echo "Pushing changes to the server and deploying AIseed..."

# Function to check for errors and retry
check_and_retry() {
    local command="$1"
    local retries=3
    local count=0

    until $command; do
        count=$((count + 1))
        if [ $count -ge $retries ]; then
            echo "Command failed after $retries attempts: $command"
            exit 1
        fi
        echo "Retrying ($count/$retries)..."
        sleep 2
    done
}

# Add all changes and commit
git add .
git commit -m "Deploying changes"

# Push to the production server
check_and_retry "git push origin main"

echo "Deployment complete!"
