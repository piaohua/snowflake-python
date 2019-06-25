#!/bin/bash

set -e

#python example.py

env FLASK_APP=example.py flask run --host=0.0.0.0 --port=8089

#curl -i -X POST http://127.0.0.1:8089/v1/id
#curl -i -X POST http://127.0.0.1:8089/v1/3493206683549701/parse
