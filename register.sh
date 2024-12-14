#!/usr/bin/bash
curl -X POST http://127.0.0.1:5000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "procode",
    "email": "moedcode@promail.com",
    "password": "procode_PWD1",
    "image": "/mnt/c/Users/Active/Pictures/Camera Roll/FB_IMG_1684853676131.jpg"
}'
