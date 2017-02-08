#coding=utf-8


# BROKER_URL = 'redis://10.0.0.12:6379/0'
BROKER_URL = 'redis://localhost:6379/0'
# BACKEND = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis'
# BACKEND= 'redis'
# CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
# CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True