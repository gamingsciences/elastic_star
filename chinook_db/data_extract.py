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


def invoice_extract(date):
    session = Session()
    q = session.query(Invoice).filter(func.date(Invoice.InvoiceDate) == date)
    results = [serialize(invoice_schema, obj) for obj in q]
    
    return results

