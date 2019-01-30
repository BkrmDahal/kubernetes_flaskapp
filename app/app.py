import os
from flask import Flask
from flask import request
import flask
import redis
import time
import json
from flask import Response, stream_with_context

app = Flask(__name__)
app.debug = True

redis_path = os.environ.get('REDIS_HOST', 'redis')
db = redis.Redis(redis_path, port=6379) #connect to server

ttl = 31104000 #one year

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@app.route('/', methods = ['PUT', 'GET'])
def cluster():
    return "welcome to cluster"

@app.route('/<path:path>/', methods = ['PUT', 'GET'])
def home(path):

    if (request.method == 'PUT'):
        event = request.json
        event['last_updated'] = int(time.time())
        event['ttl'] = ttl
        db.delete(path) #remove old keys
        db.set(path, event[path])
        db.expire(path, ttl)
        return json.dumps({"message" :"success",
                           "data": event}), 201

    if not db.exists(path):
        return "Error: thing doesn't exist"

    event = db.get(path)
    return json.dumps({"message": "success", 
                       path: event.decode('utf-8')}), 200


if __name__ == "__main__":
    app.run()