#coding=utf-8
from celery import Celery
from forest.settings.final_settings import default_scheduler_settings_path
C=Celery()
C.config_from_object(default_scheduler_settings_path)
