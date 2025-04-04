#!/bin/bash

echo "Automating GitHub repository creation, CI/CD pipeline setup, and deployment..."

# Variables
GITHUB_USERNAME="mrpongalfer"
REPO_NAME="AIseed"
SERVER_IP="192.168.0.95"
SERVER_USER="aiseed"
SERVER_PROJECT_DIR="/home/aiseed/AIseed"
BRANCH="main"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed. Installing..."
    sudo apt update
    sudo apt install -y gh
fi

# Authenticate GitHub CLI
echo "Authenticating GitHub CLI..."
gh auth login

# Create GitHub repository
echo "Creating GitHub repository..."
gh repo create "$GITHUB_USERNAME/$REPO_NAME" --public --source=. --remote=origin --push

# Initialize Git repository locally
echo "Initializing Git repository locally..."
rm -rf .git  # Remove any existing Git repository to avoid conflicts
git init
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git add .
git commit -m "Initial commit"
git branch -M "$BRANCH"
git push -u origin "$BRANCH"

# Set up CI/CD pipeline
echo "Setting up CI/CD pipeline..."
mkdir -p .github/workflows
cat <<EOF > .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - $BRANCH
  pull_request:
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
git push

# Generate SSH key for GitHub Actions
echo "Generating SSH key for GitHub Actions..."
ssh-keygen -t rsa -b 4096 -C "github-actions@$GITHUB_USERNAME" -f github-actions-key -N ""
echo "Public key for GitHub Actions:"
cat github-actions-key.pub

# Add the public key to the server's authorized_keys
echo "Adding public key to the server's authorized_keys..."
ssh-copy-id -i github-actions-key.pub $SERVER_USER@$SERVER_IP

# Add the private key to GitHub repository secrets
echo "Adding private key to GitHub repository secrets..."
echo "Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/secrets/actions"
echo "Add a new secret with the name 'SSH_PRIVATE_KEY' and paste the contents of github-actions-key."

# Final instructions
echo "Setup complete! Push changes to trigger the CI/CD pipeline."
echo "Monitor the pipeline in the Actions tab of your GitHub repository."
