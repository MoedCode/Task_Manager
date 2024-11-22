#!/usr/bin/env python3

import requests

# Define the URL and the token
url = "http://127.0.0.1:5000/"
token = "ddaf56ad711478bb325bc610892e9cff30093724b4aebb31809b321ab1fe91b2"

# Define headers with the token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Send a GET request to the server
response = requests.get(url, headers=headers)

# Print the response from the server
print(response.status_code)
print(response.text)

