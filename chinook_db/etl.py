# -*- coding: utf-8 -*-
"""
The ETL function for ElasticStar.

Created on Sat Nov  5 16:04:10 2016

@author: ken
"""
#import datetime
#from preserialize.serialize import serialize
from django.conf import settings
from .data_extract import extract_by_date
from .transform import batch_transform
from elasticsearch import Elasticsearch, helpers


es_host = settings.ES_HOST

def etl(audit_date, model):
    '''
    The ETL function. Uses the Dict 'extract_funcs' and the data_type var
    must be a key in this dict.
    '''
    es = Elasticsearch([es_host])
    batch_chunks = []
    iterator = 0
    ext = extract_by_date(audit_date, model)
    trans = batch_transform(model, audit_date, ext)
    for rec in trans:
        data_dict = {
                "_index": rec["index"],
                "_type": rec["type"],
                "_id": rec["id"],
                "_source": rec["body"]
        }

        batch_chunks.append(data_dict)
        if iterator % 100 == 0:
            helpers.bulk(es, batch_chunks, request_timeout=60)
            del batch_chunks[:]
        iterator = iterator + 1

    if len(batch_chunks) != 0:
        helpers.bulk(es, batch_chunks)
