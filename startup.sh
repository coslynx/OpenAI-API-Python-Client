#!/bin/bash
set -euo pipefail

# Load environment variables from .env file
source .env

# Check if environment variables are set
if [[ -z "$OPENAI_API_KEY" ]]; then
  echo "Error: OPENAI_API_KEY environment variable is not set."
  exit 1
fi

if [[ -z "$DATABASE_URL" ]]; then
  echo "Error: DATABASE_URL environment variable is not set."
  exit 1
fi

if [[ -z "$SECRET_KEY" ]]; then
  echo "Error: SECRET_KEY environment variable is not set."
  exit 1
fi

# Initialize the database
alembic upgrade head

# Start the application server using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000