# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:17:55 2016

@author: Lathropk
"""
from celery import shared_task
import datetime
import pandas as pd
from dateutil.parser import parse
from .etl import etl
from .models import *
from utils.loggers import UpdateElasticLogger
from utils.timezone_utils import utc_to_local
from django.conf import settings
from elasticsearch import Elasticsearch

es_host = settings.ES_HOST

logger = UpdateElasticLogger()
elastic_logger = logger.myLogger()


def update_recs(model):
    elastic_logger.info("Updating elasticsearch %s Documents" % model.es_index )
    try:
        es = Elasticsearch([es_host])
        query = {
            'query': {
                'match_all': {},
            },
            'sort': {
                    model.es_date_field: {"order": "desc"}
            },
            'size': '1'
        }
        res = es.search(index=model.es_index, body=query)

        d = res['hits']['hits'][0]['_source'][model.es_date_field]
        last_update = utc_to_local(parse(d))
        start_date = last_update + datetime.timedelta(days=1)
        today = datetime.datetime.now().date()
        end_date = today - datetime.timedelta(days=1)
        if start_date == end_date:
            etl(start_date, model)
        else:
            dates = pd.date_range(start_date, end_date).tolist()
            for date in dates:
                etl(date, model)
    except Exception as e:
            elastic_logger.exception(e)
    elastic_logger.info("Update complete")

@shared_task
def update_all():
    update_recs(invoice)
