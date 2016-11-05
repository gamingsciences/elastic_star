# -*- coding: utf-8 -*-
"""
The data_extract program uses Sqlalchemy automap to reflect the target 
database.  Marshmallow is then used to serialize the data.

It is the first part in the ETL process for ElasticStar.

Created on Sat Feb 06 15:48:10 2016

@author: Lathropk
"""
from sqlalchemy import func
from .models import Session, Invoice
from .schemas import invoice_schema
from utils.database_utils import serialize
from utils.loggers import ChinookExtractLogger

logger = ChinookExtractLogger()
extract_logger = logger.myLogger()

def invoice_extract(date):
    index = 'chinook_invoice'
    type_ = 'invoice'
    extract_logger.info("Extracting invoice records for %s" %date )
    session = Session()
    try:
        q = session.query(Invoice).filter(func.date(Invoice.InvoiceDate) == date)
        results = [{'index': index, 
                'type': type_,                
                'body': serialize(invoice_schema, obj)} for obj in q]
        extract_logger.info("Extract successful")
        return results
        
    except Exception as e:
        extract_logger.info("Error extracting invoice data for %s" % date)
        extract_logger.error(e, exec_info=True)    
    

