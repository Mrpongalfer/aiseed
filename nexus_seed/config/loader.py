import os
import json
from typing import Dict

def load_config(json_path: str) -> Dict:
    """
    Load configuration from a JSON file and override with environment variables.
    """
    try:
        with open(json_path, "r") as file:
            config = json.load(file)
        
        # Override with environment variables
        for key, value in os.environ.items():
            if key.startswith("NEXUS_"):
                nested_keys = key.replace("NEXUS_", "").lower().split("__")
                current = config
                for k in nested_keys[:-1]:
                    current = current.setdefault(k, {})
                current[nested_keys[-1]] = value

        # Construct the database URL dynamically
        db_config = config.get("database", {})
        config["database"]["db_url"] = (
            f"postgresql://{db_config.get('username')}:{db_config.get('password')}"
            f"@{db_config.get('host')}:{db_config.get('port')}/{db_config.get('database_name')}"
        )

        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}
