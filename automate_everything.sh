#!/bin/bash

echo "Automating AIseed setup, CI/CD pipeline configuration, and deployment..."

# Variables
GITHUB_USERNAME="mrpongalfer"
REPO_NAME="aiseed"
SERVER_IP="192.168.0.95"
SERVER_USER="aiseed"
SERVER_PROJECT_DIR="/home/aiseed/AIseed"
BRANCH="main"
SSH_KEY_NAME="github-actions-key"

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

# Step 1: Install Required Tools
echo "Installing required tools..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose git gh sshpass

# Step 2: Authenticate GitHub CLI
echo "Authenticating GitHub CLI..."
check_and_retry "gh auth login"

# Step 3: Initialize Git Repository
echo "Initializing Git repository..."
rm -rf .git  # Remove any existing Git repository to avoid conflicts
git init

# Step 4: Configure Git Remote
echo "Configuring Git remote to use HTTPS..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

git add .
git commit -m "Initial commit"
git branch -M "$BRANCH"
check_and_retry "git push -u origin $BRANCH"

# Step 5: Set Up CI/CD Pipeline
echo "Setting up CI/CD pipeline..."
mkdir -p .github/workflows
cat <<EOF > .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - $BRANCH

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint code
        run: |
          source .venv/bin/activate
          flake8 .

      - name: Run tests
        run: |
          source .venv/bin/activate
          pytest --asyncio-mode=auto tests/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to Server
        env:
          SSH_PRIVATE_KEY: \${{ secrets.SSH_PRIVATE_KEY }}
        run: |
          mkdir -p ~/.ssh
          echo "\$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H $SERVER_IP >> ~/.ssh/known_hosts
          rsync -avz --exclude '.venv' --exclude '.git' . $SERVER_USER@$SERVER_IP:$SERVER_PROJECT_DIR
          ssh $SERVER_USER@$SERVER_IP "bash $SERVER_PROJECT_DIR/startup.sh"
EOF

# Push CI/CD configuration
git add .github/workflows/deploy.yml
git commit -m "Add CI/CD pipeline"
check_and_retry "git push"

# Step 6: Regenerate SSH Key for GitHub Actions
echo "Regenerating SSH key for GitHub Actions..."
rm -f $SSH_KEY_NAME $SSH_KEY_NAME.pub  # Remove existing keys
ssh-keygen -t rsa -b 4096 -C "github-actions@$GITHUB_USERNAME" -f $SSH_KEY_NAME -N ""
echo "Public key for GitHub Actions:"
cat $SSH_KEY_NAME.pub

# Add the public key to the server's authorized_keys
echo "Adding public key to the server's authorized_keys..."
sshpass -p "your-server-password" ssh-copy-id -i $SSH_KEY_NAME.pub $SERVER_USER@$SERVER_IP

# Add the private key to GitHub repository secrets
echo "Adding private key to GitHub repository secrets..."
echo "Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/secrets/actions"
echo "Add a new secret with the name 'SSH_PRIVATE_KEY' and paste the contents of $SSH_KEY_NAME."

# Step 7: Set Up Server Environment
echo "Setting up server environment..."
ssh $SERVER_USER@$SERVER_IP <<EOF
sudo apt update
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose git
mkdir -p $SERVER_PROJECT_DIR
EOF

# Step 8: Final Instructions
echo "Setup complete! Push changes to trigger the CI/CD pipeline."
echo "Monitor the pipeline in the Actions tab of your GitHub repository."
