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


from utils.loggers import UpdateElasticLogger
from utils.timezone_utils import utc_to_local
from django.conf import settings

from elasticsearch import Elasticsearch

es_host = settings.ES_HOST

logger = UpdateElasticLogger()
elastic_logger = logger.myLogger()


@shared_task
def update_invoice_recs():
    elastic_logger.info("Updating elasticsearch Chinook Invoice Documents" )
    try:
        es = Elasticsearch([es_host])
        query = {
            'query': {
                'match_all': {},
            },
            'sort': {
                    'InvoiceDate': {"order": "desc"}
            },
            'size': '1'
        }
        res = es.search(index='chinook_invoice', body=query)
        
        d = res['hits']['hits'][0]['_source']['InvoiceDate']
        last_update = utc_to_local(parse(d))
        start_date = last_update + datetime.timedelta(days=1)
        today = datetime.datetime.now().date()
        end_date = today - datetime.timedelta(days=1)
        if start_date == end_date:
            etl(start_date, "invoice")
        else:
            dates = pd.date_range(start_date, end_date).tolist()
            for date in dates:
                etl(date, "invoice")
    except Exception as e:
            elastic_logger.exception(e)
    elastic_logger.info("Update complete")

@shared_task
def update_invoiceline_recs():
    elastic_logger.info("Updating elasticsearch Chinook InvoiceLine Documents" )
    try:
        es = Elasticsearch([es_host])
        query = {
            'query': {
                'match_all': {},
            },
            'sort': {
                    'invoice.InvoiceDate': {"order": "desc"}
            },
            'size': '1'
        }
        res = es.search(index='chinook_invoiceline', body=query)
        
        d = res['hits']['hits'][0]['_source']['Invoice']['InvoiceDate']
        last_update = utc_to_local(parse(d))
        start_date = last_update + datetime.timedelta(days=1)
        today = datetime.datetime.now().date()
        end_date = today - datetime.timedelta(days=1)
        if start_date == end_date:
            etl(start_date, "invoiceline")
        else:
            dates = pd.date_range(start_date, end_date).tolist()
            for date in dates:
                etl(date, "invoiceline")
    except Exception as e:
            elastic_logger.exception(e)
    elastic_logger.info("Update complete")