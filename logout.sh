#!/bin/bash

# Check if a token was provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <token>"
  exit 1
fi

# Variables
TOKEN=$1
URL="http://127.0.0.1:5000/api/logout/"

# Make the POST request
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$URL" \
  -H "Authorization: Bearer $TOKEN")

# Handle the response
if [ "$response" -eq 200 ]; then
  echo "Logout successful."
elif [ "$response" -eq 400 ]; then
  echo "Error: Invalid token or missing Authorization header."
else
  echo "Error: Received HTTP status code $response."
fi
