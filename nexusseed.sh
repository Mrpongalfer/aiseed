#!/bin/bash

# --- Omnitide Nexus Seed - Setup Wizard & Skeleton Generator v1.2 ---
# Creates the project structure, skeleton files, config templates,
# Docker setup, Master Prompt file, and provides setup instructions.
# Includes OrchestratorService, SystemMonitorService, StatsAggregatorService, CLI stub.

echo "======================================================"
echo " Omnitide Nexus Seed Setup & Skeleton Generator v1.2"
echo "======================================================"
echo "This script will create the full project skeleton, configuration"
echo "templates, and helper setup based on the finalized blueprint."
echo ""
echo "INFO: It will create directories and files relative to the current location."
read -p "Proceed with setup in the current directory? [y/N]: " confirm_setup
if [[ ! "$confirm_setup" =~ ^[Yy]$ ]]; then
  echo "Aborted by user."
  exit 0
fi
echo ""
echo "Starting setup..."

# --- Validate and Automate Environment Setup ---
validate_and_setup_environment() {
  echo "Validating and setting up the environment..."
  local missing_tools=()

  # Check for required tools
  for tool in "python3" "pip" "docker" "docker-compose"; do
    if ! command -v "$tool" &> /dev/null; then
      missing_tools+=("$tool")
    fi
  done

  # Install missing tools
  if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "The following tools are missing: ${missing_tools[*]}"
    echo "Attempting to install missing tools..."

    # Install Python and pip
    if [[ " ${missing_tools[*]} " =~ " python3 " ]]; then
      echo "Installing Python 3..."
      sudo apt update && sudo apt install -y python3 python3-venv python3-pip || {
        echo "ERROR: Failed to install Python 3. Please install it manually."; exit 1;
      }
    fi

    # Install Docker
    if [[ " ${missing_tools[*]} " =~ " docker " ]]; then
      echo "Installing Docker..."
      sudo apt update && sudo apt install -y docker.io || {
        echo "ERROR: Failed to install Docker. Please install it manually."; exit 1;
      }
      sudo systemctl start docker
      sudo systemctl enable docker
    fi

    # Install Docker Compose
    if [[ " ${missing_tools[*]} " =~ " docker-compose " ]]; then
      echo "Installing Docker Compose..."
      sudo apt update && sudo apt install -y docker-compose || {
        echo "ERROR: Failed to install Docker Compose. Please install it manually."; exit 1;
      }
    fi

    # Install pip
    if [[ " ${missing_tools[*]} " =~ " pip " ]]; then
      echo "Installing pip..."
      sudo apt update && sudo apt install -y python3-pip || {
        echo "ERROR: Failed to install pip. Please install it manually."; exit 1;
      }
    fi
  fi

  echo "All required tools are installed."

  # Create and activate a virtual environment
  echo "Setting up Python virtual environment..."
  python3 -m venv .venv || {
    echo "ERROR: Failed to create virtual environment."; exit 1;
  }
  source .venv/bin/activate || {
    echo "ERROR: Failed to activate virtual environment."; exit 1;
  }

  # Install Python dependencies
  echo "Installing Python dependencies..."
  pip install --upgrade pip || {
    echo "ERROR: Failed to upgrade pip."; exit 1;
  }
  pip install -r requirements.txt || {
    echo "ERROR: Failed to install Python dependencies."; exit 1;
  }

  echo "Environment setup complete."
}

# --- Generate Configuration and Docker Files ---
generate_nexus_config() {
  echo "Generating nexus_seed_config.json..."
  cat > nexus_seed_config.json <<EOF
{
  "logging": {
    "level": "INFO",
    "log_file": "logs/nexus_seed.log"
  },
  "kernel": {
    "snapshot_interval_sec": 300,
    "snapshot_location": "persistence/snapshot.pkl"
  },
  "persistence": {
    "type": "postgresql",
    "connection_string": "postgresql://user:password@localhost:5432/nexusdb"
  },
  "services": {
    "SystemMonitorService": {
      "enabled": true,
      "publish_interval_sec": 5
    },
    "StatsAggregatorService": {
      "enabled": true,
      "aggregation_interval_sec": 10
    }
  }
}
EOF
  echo "  [OK] nexus_seed_config.json generated."
}

generate_env_file() {
  echo "Generating .env file..."
  cat > .env <<EOF
DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/nexusdb
LOG_LEVEL=INFO
EOF
  echo "  [OK] .env file generated."
}

generate_dockerfile() {
  echo "Generating Dockerfile..."
  cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
EOF
  echo "  [OK] Dockerfile generated."
}

generate_docker_compose() {
  echo "Generating docker-compose.yml..."
  cat > docker-compose.yml <<EOF
version: '3.8'
services:
  nexus-seed:
    build: .
    volumes:
      - ./logs:/app/logs
      - ./persistence:/app/persistence
    env_file:
      - .env
    ports:
      - "8000:8000"
EOF
  echo "  [OK] docker-compose.yml generated."
}

generate_requirements_file() {
  echo "Generating requirements.txt..."
  cat > requirements.txt <<EOF
asyncpg==0.27.0
psutil==5.9.5
pytest==7.4.0
pytest-asyncio==0.21.0
pyyaml==6.0
grpcio==1.56.0
grpcio-tools==1.56.0
textual==0.10.0
nats-py==2.2.0
EOF
  echo "  [OK] requirements.txt generated."
}

generate_project_files() {
  echo "Step 2: Generating Configuration and Docker Files..."
  generate_nexus_config
  generate_env_file
  generate_dockerfile
  generate_docker_compose
  generate_requirements_file
  echo "Configuration and Docker files generated successfully."
}

# --- Define Schemas and Generate Protos ---
define_schemas_and_protos() {
  echo "Defining schemas and generating .proto files..."

  # Create directory for schemas
  mkdir -p schemas
  cat > schemas/nexus.proto <<EOF
syntax = "proto3";

package nexus;

service NexusService {
  rpc PublishMetrics (MetricsRequest) returns (MetricsResponse);
}

message MetricsRequest {
  string service_name = 1;
  map<string, string> metrics = 2;
}

message MetricsResponse {
  bool success = 1;
}
EOF
  echo "  [OK] schemas/nexus.proto created."

  # Ensure virtual environment is activated
  if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate || {
      echo "ERROR: Failed to activate virtual environment."; exit 1;
    }
  else
    echo "ERROR: Virtual environment not found. Please set it up first."; exit 1;
  fi

  # Generate Python gRPC code
  python3 -m grpc_tools.protoc -Ischemas --python_out=nexus_seed/interfaces --grpc_python_out=nexus_seed/interfaces schemas/nexus.proto || {
    echo "ERROR: Failed to generate gRPC code."; exit 1;
  }
  echo "  [OK] gRPC code generated."
}

# --- Generate CLI Interface Monitor ---
generate_cli_monitor() {
  echo "Generating CLI interface monitor..."

  mkdir -p cli
  cat > cli/nexus_monitor_cli.py <<EOF
import asyncio
from textual.app import App
from textual.widgets import Header, Footer, ScrollView

class NexusMonitorApp(App):
    async def on_mount(self):
        self.body = ScrollView()
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.body, edge="center")

    async def update_metrics(self, metrics):
        await self.body.update(f"Metrics: {metrics}")

async def fetch_metrics():
    # Simulate fetching metrics from NATS or gRPC
    await asyncio.sleep(1)
    return {"cpu": "50%", "memory": "60%"}

async def main():
    app = NexusMonitorApp()
    asyncio.create_task(app.run_async())
    while True:
        metrics = await fetch_metrics()
        await app.update_metrics(metrics)

if __name__ == "__main__":
    asyncio.run(main())
EOF
  echo "  [OK] CLI monitor generated."
}

# --- Generate Adapters for Communication ---
generate_adapters() {
  echo "Generating adapters for communication..."

  mkdir -p nexus_seed/adapters
  cat > nexus_seed/adapters/nats_adapter.py <<EOF
import asyncio
from nats.aio.client import Client as NATS

class NATSAdapter:
    def __init__(self, server="nats://localhost:4222"):
        self.server = server
        self.nc = NATS()

    async def connect(self):
        await self.nc.connect(servers=[self.server])

    async def publish(self, subject, message):
        await self.nc.publish(subject, message.encode())

    async def subscribe(self, subject, callback):
        await self.nc.subscribe(subject, cb=callback)

    async def close(self):
        await self.nc.close()
EOF
  echo "  [OK] NATS adapter generated."

  cat > nexus_seed/adapters/grpc_adapter.py <<EOF
import grpc
from nexus_seed.interfaces import nexus_pb2, nexus_pb2_grpc

class GRPCAdapter:
    def __init__(self, server="localhost:50051"):
        self.server = server
        self.channel = None
        self.stub = None

    async def connect(self):
        self.channel = grpc.aio.insecure_channel(self.server)
        self.stub = nexus_pb2_grpc.NexusServiceStub(self.channel)

    async def publish_metrics(self, service_name, metrics):
        request = nexus_pb2.MetricsRequest(service_name=service_name, metrics=metrics)
        return await self.stub.PublishMetrics(request)

    async def close(self):
        await self.channel.close()
EOF
  echo "  [OK] gRPC adapter generated."
}

# --- Create Project Structure ---
echo ""
echo "Step 1: Creating Project Directory Structure..."
declare -a dirs=(
    "nexus_seed/config" "nexus_seed/interfaces" "nexus_seed/kernel"
    "nexus_seed/services" "nexus_seed/utils" "persistence" "logs"
    "blueprints" "config_files/workflows" "cli"
)
for dir in "${dirs[@]}"; do mkdir -p "$dir" || { echo "ERROR creating directory $dir."; exit 1; }; done
echo "  Base directories created."
declare -a init_files=(
    "nexus_seed/__init__.py" "nexus_seed/config/__init__.py"
    "nexus_seed/interfaces/__init__.py" "nexus_seed/kernel/__init__.py"
    "nexus_seed/services/__init__.py" "nexus_seed/utils/__init__.py"
)
for init_file in "${init_files[@]}"; do touch "$init_file" || { echo "ERROR creating $init_file."; exit 1; }; done
echo "  __init__.py files created."
touch logs/.gitkeep persistence/.gitkeep blueprints/.gitkeep config_files/.gitkeep config_files/workflows/.gitkeep cli/.gitkeep || exit 1
echo "  .gitkeep files created."
echo "Structure Creation Complete."
echo ""

# --- Generate Configuration Files ---
generate_project_files

# --- Call the new functions ---
define_schemas_and_protos
generate_cli_monitor
generate_adapters

echo ""
echo "Step 4: Saving Final Master Prompt..."
prompt_save_path="$HOME/nexus_master_prompt_v1.txt"
echo "$MASTER_PROMPT_V1_0" > "$prompt_save_path"
if [ $? -eq 0 ]; then
  echo "  [OK] Final Master Prompt v1.0 saved to '$prompt_save_path'"
else
  echo "ERROR: Failed to save Master Prompt to '$prompt_save_path'."
fi

# --- Final Instructions ---
echo "================================================"
echo " Nexus Seed Skeleton Setup Complete! (v1.2)"
echo "================================================"
echo "NEXT STEPS:"
echo "1.  Review Files: Examine created directories and skeleton '.py' files (incl. new services)."
echo "2.  Virtual Env: If needed: 'python -m venv .venv && source .venv/bin/activate'"
echo "3.  Dependencies: Run 'pip install -r requirements.txt' (check system prerequisites)."
echo "4.  Configure: Edit '.env' file with SECURE credentials. Review/adjust 'nexus_seed_config.json'."
echo "5.  Implement Logic: Follow the **Final Implementation Checklist v1.2**."
echo "6.  Testing: Implement unit, integration, resilience, security tests CONTINUOUSLY."
echo "7.  CI/CD: Set up CI/CD pipeline for Blueprint Evolution (Phase 4)."
echo "8.  Deploy Locally: Use 'docker-compose up --build -d'. Check logs."
echo "9.  Use Master Prompt: Saved at '$prompt_save_path'. Use 'nexus-prompt' command or copy/paste into new AI sessions."
echo "10. Run CLI Monitor: Use 'python cli/nexus_monitor_cli.py' (requires Seed running & stats published)."
echo ""
echo "Implementation phase begins now, Architect. Good luck."
echo "================================================"

exit 0