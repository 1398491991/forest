from flask import Flask
from flask import request
from forest.http.request import Request
from forest.utils.serializable import load_json
from forest.services.add import AddRequest

app =Flask(__name__)


@app.route('/addRequest',methods=['POST'])
def add_request():
    j=request.get_json()
    if not j:
        return {"type error"}
    try:
        addRequest=AddRequest.from_json(j)
        addRequest.add()
        return {"succeed"}
    except:
        return {"add error"}

