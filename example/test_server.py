#coding=utf-8

from flask import Flask
from flask import Response

app=Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return Response('hello')

if __name__ == '__main__':
    app.run(debug=True)