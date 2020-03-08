# A very simple Flask Hello World app for you to get started with...
from flask import Flask, escape, request
app = Flask(__name__)

@app.route('/api/')
def hello_world():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
