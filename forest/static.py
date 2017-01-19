from queue import Queue,PriorityQueue
from rd import rd_conn
from config import config

slave_name=''
queue=Queue(rd_conn)
priority_queue=PriorityQueue(rd_conn)


appoint_queue_key=config.get('queue','private_queue')%slave_name
public_priority_queue_key=config.get('queue','public_priority_queue')
public_queue_key=config.get('queue','public_queue')