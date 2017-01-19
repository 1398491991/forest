from flask import Flask
from flask import request
from ..worker.scheduler import enqueue_scheduler
from ..http.request import Request
from ..utils.serializable import load_json

app =Flask(__name__)


@app.route('/addRequest',methods=['POST'])
def add_request():
    j=request.get_json()
    if not j:
        return {"type error"}
    try:
        enqueue_scheduler.scheduler(Request(**load_json(j)))
        return {"succeed"}
    except:
        return {"init error"}

