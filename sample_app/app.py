import os
from flask import Flask
from flask import request
import flask
import redis
import time
import json
from flask import Response, stream_with_context

app = Flask(__name__)


@app.route('/api/')
def cluster():
    return "welcome to cluster /api/"

@app.route('/api/<welcome>')
def cluster_2(welcome):
    return "welcome to cluster /api/ " + welcome

@app.route('/')
def cluster_1():
    return "welcome to cluster"


if __name__ == "__main__":
    app.run()
