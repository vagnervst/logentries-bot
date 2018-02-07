# RUN WITH FLASK_APP=flask.py flask run

from flask import Flask
from flask import request
import json

app = Flask(__name__)

class Response(object):
    def __init__(self, code, content):
        self.code = code
        self.content = content

class Customer(object):
    def __init__(self, name):
        self.name = name

@app.route("/", methods=["GET", "POST", "PUT"])
def getCustomer():
    if request.method == 'POST':
        customer = Customer('Chavo')
        response = Response(200, json.dumps(customer.__dict__))
        return json.dumps(response.__dict__)
    elif request.method == 'PUT':
        customer = Customer('Chiquinha')
        response = Response(200, json.dumps(customer.__dict__))
        return json.dumps(response.__dict__)
    else:
        customer = Customer('Madruga')
        response = Response(200, json.dumps(customer.__dict__))
        return json.dumps(response.__dict__)
