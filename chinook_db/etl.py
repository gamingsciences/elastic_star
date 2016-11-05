# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 16:04:10 2016

@author: ken
"""
#import datetime
#from preserialize.serialize import serialize
from django.conf import settings
from .data_extract import invoice_extract
from .transform import batch_transform
from elasticsearch import Elasticsearch, helpers

es_host = settings.ES_HOST

def invoice_etl(audit_date):
    es = Elasticsearch([es_host])
    batch_chunks = []
    iterator = 0
    invoice_ext = invoice_extract(audit_date)
    invoice_trans = batch_transform(audit_date, invoice_ext)
    for invoice in invoice_trans:
        s = invoice
        data_dict = {
                "_index": s["index"], 
                "_type": s["type"],
                "_id": s["body"]["InvoiceId"],
                "_source": s["body"]
        }
        
        batch_chunks.append(data_dict)
        if iterator % 100 == 0:
            helpers.bulk(es, batch_chunks, request_timeout=60)
            del batch_chunks[:]
        iterator = iterator + 1
    
    if len(batch_chunks) != 0:
        helpers.bulk(es, batch_chunks)
