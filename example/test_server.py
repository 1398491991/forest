#coding=utf-8

from flask import Flask
from flask import Response

app=Flask(__name__)

@app.route('/<name>', methods=['GET'])
def index(name):
    return Response(name)

if __name__ == '__main__':
    app.run(debug=True)