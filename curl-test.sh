#!/bin/bash

curl --request POST http://localhost:5000/api/timeline_post -d 'name=Elaine&email=eleiyoun@bu.edu&content=Checking GET and POST endpoints'

curl http://localhost:5000/api/timeline_post
