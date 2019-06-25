#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from datetime import timedelta
import sys
sys.path.append("..")
import snowflake

KEY = "48a6ebac4ebc6642d68c217fca33eb4d"

app = Flask(__name__)
app.secret_key = KEY
app.config['SESSION_TYPE'] = 'memcached'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
app.config.update(
    DEBUG=True,
)

sf = snowflake.generate(0, 0)

@app.route('/v1/id', methods=["POST"])
def id():
    id = sf.next()
    result = {"id": id}
    return json.dumps(result)

@app.route('/v1/<int:id>/parse', methods=["POST"])
def parse(id):
    result = snowflake.parse(id)
    return json.dumps(result)

if __name__ == '__main__':
    app.secret_key = KEY
    app.run(host='0.0.0.0', port=8089)
