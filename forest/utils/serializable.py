import json
import pickle

def load_json(j,**kwargs):
    return json.loads(j,**kwargs)

def load_pickle(p,**kwargs):
    return pickle.loads(p,**kwargs)

def dump_json(j,**kwargs):
    return json.dumps(j,**kwargs)

def dump_pickle(p,**kwargs):
    return pickle.dumps(p,**kwargs)