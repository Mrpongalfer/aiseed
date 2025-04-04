import json

class SetupWizard:
    @staticmethod
    def run():
        try:
            print("======================================================")
            print(" Welcome to the Nexus Core Interactive Setup Wizard!")
            print("======================================================")
            print("This wizard will guide you through configuring the Nexus Core.")
            print("")

            # Step 1: Configure Logging
            print("Step 1: Configure Logging")
            logging_level = input("Enter logging level (default: INFO): ") or "INFO"
            log_file = input("Enter log file path (default: logs/nexus_seed.log): ") or "logs/nexus_seed.log"
            print("")

            # Step 2: Configure Persistence
            print("Step 2: Configure Persistence")
            print("Choose a persistence type:")
            print("1. PostgreSQL (recommended for production)")
            print("2. SQLite (lightweight, for local testing)")
            persistence_choice = input("Enter your choice (1/2, default: 1): ") or "1"
            if persistence_choice == "1":
                persistence_type = "postgresql"
                connection_string = input("Enter PostgreSQL connection string (default: postgresql://user:password@localhost:5432/nexusdb): ") or "postgresql://user:password@localhost:5432/nexusdb"
            else:
                persistence_type = "sqlite"
                connection_string = "sqlite:///nexusdb.sqlite"
            print("")

            # Step 3: Configure Services
            print("Step 3: Configure Services")
            system_monitor_enabled = SetupWizard._get_boolean_input("Enable SystemMonitorService? (y/n, default: y): ", True)
            system_monitor_interval = int(input("Enter publish interval (seconds, default: 5): ") or 5) if system_monitor_enabled else None

            stats_aggregator_enabled = SetupWizard._get_boolean_input("Enable StatsAggregatorService? (y/n, default: y): ", True)
            stats_aggregator_interval = int(input("Enter aggregation interval (seconds, default: 10): ") or 10) if stats_aggregator_enabled else None
            print("")

            # Step 4: Generate Configuration Files
            print("Step 4: Generating Configuration Files...")
            config = {
                "logging": {
                    "level": logging_level,
                    "log_file": log_file
                },
                "kernel": {
                    "snapshot_interval_sec": 300,
                    "snapshot_location": "persistence/snapshot.pkl"
                },
                "persistence": {
                    "type": persistence_type,
                    "connection_string": connection_string
                },
                "services": {
                    "SystemMonitorService": {
                        "enabled": system_monitor_enabled,
                        "publish_interval_sec": system_monitor_interval
                    },
                    "StatsAggregatorService": {
                        "enabled": stats_aggregator_enabled,
                        "aggregation_interval_sec": stats_aggregator_interval
                    }
                }
            }
            with open("nexus_seed_config.json", "w") as config_file:
                json.dump(config, config_file, indent=2)
            print("  [OK] nexus_seed_config.json generated.")

            # Step 5: Generate .env File
            print("Step 5: Generating .env File...")
            with open(".env", "w") as env_file:
                env_file.write(f"DB_CONNECTION_STRING={connection_string}\nLOG_LEVEL={logging_level}\n")
            print("  [OK] .env file generated.")

            print("")
            print("Setup Wizard Complete! Configuration files have been generated.")
            print("You can now proceed to deploy the Nexus Core.")
            print("======================================================")
        except Exception as e:
            print(f"Error during setup: {e}")

    @staticmethod
    def _get_boolean_input(prompt: str, default: bool) -> bool:
        response = input(prompt).strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        return default
