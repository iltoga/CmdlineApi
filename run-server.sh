#!/bin/bash

# Start Docker Compose services in the background
docker compose up -d

# # Wait for Docker services to be fully up and running
# # You might need to adjust the sleep duration based on your setup
# sleep 10

# # Run the Uvicorn server
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
