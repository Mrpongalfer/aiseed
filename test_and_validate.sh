#!/bin/bash

echo "Testing and validating the AIseed system..."

# Run tests
pytest --asyncio-mode=auto tests/

# Validate CI/CD pipeline
python -c "
from nexus_seed.services.validation_service import ValidationService
pipeline_config = {
    'name': 'CI/CD Pipeline',
    'on': {'push': {'branches': ['main']}},
    'jobs': {'build': {}, 'deploy': {}}
}
validator = ValidationService(None)
if not validator.validate_pipeline(pipeline_config):
    print('Pipeline validation failed.')
    exit(1)
else:
    print('Pipeline validation passed.')
"

echo "Testing and validation complete!"
