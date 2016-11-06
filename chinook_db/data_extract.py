# -*- coding: utf-8 -*-
"""
The data_extract program uses Sqlalchemy automap to reflect the target 
database.  Marshmallow is then used to serialize the data.

It is the first part in the ETL process for ElasticStar.

Created on Sat Feb 06 15:48:10 2016

@author: Lathropk
"""
from sqlalchemy import func
from .models import Session, Invoice, InvoiceLine
from .schemas import invoice_schema, invoiceline_schema
from utils.database_utils import serialize
from utils.loggers import ExtractLogger

logger = ExtractLogger()
extract_logger = logger.myLogger()

def invoice_extract(date):
    '''
    Extracts Invoice data from the Chinook DB.
    Uses the InvoiceId field for the Elasticsearch id.
    '''
    index = 'chinook_invoice'
    type_ = 'invoice'
    extract_logger.info("Extracting chinook invoice records for %s" %date )
    session = Session()
    try:
        q = session.query(Invoice).filter(func.date(Invoice.InvoiceDate) == date)
        results = [{'index': index, 
                'type': type_,                
                'body': serialize(invoice_schema, obj),
                'id':obj.InvoiceId} for obj in q]
                
        extract_logger.info("Extract successful")
        return results
        
    except Exception as e:
        extract_logger.info("Error extracting chinook invoice data for %s" % date)
        extract_logger.error(e, exec_info=True)
        
def invoiceline_extract(date):
    '''
    Extracts InvoiceLine data from the Chinook DB.
    Uses the InvoiceLineId field for the Elasticsearch id.
    '''
    index = 'chinook_invoiceline'
    type_ = 'invoiceline'
    extract_logger.info("Extracting chinook invoiceline records for %s" %date )
    session = Session()
    try:
        q = session.query(InvoiceLine).join(Invoice)\
                .filter(func.date(Invoice.InvoiceDate) == date)
        
        results = [{'index': index, 
                'type': type_,                
                'body': serialize(invoiceline_schema, obj),
                'id':obj.InvoiceLineId} for obj in q]
                
        extract_logger.info("Extract successful")
        return results
        
    except Exception as e:
        extract_logger.info("Error extracting chinook invoiceline data for %s" % date)
        extract_logger.error(e)

# This is the dict that is passed to the transform function     
extract_funcs = {'invoice': invoice_extract,
                 'invoiceline': invoiceline_extract}

