# -*- coding: utf-8 -*-
"""
The data_extract program uses Sqlalchemy automap to reflect the target
database.  Marshmallow is then used to serialize the data.

It is the first part in the ETL process for ElasticStar.

Created on Sat Feb 06 15:48:10 2016

@author: Lathropk
"""
import os
from sqlalchemy import func
from .models import Session
from utils.database_utils import serialize
from utils.loggers import ExtractLogger

logger = ExtractLogger()
extract_logger = logger.myLogger()

def extract_by_date(model, date):
    '''
    Extracts Model data from the DB.

    '''
    dir_name = os.path.dirname(os.path.abspath(__file__))
    index = model.es_index
    type_ = model.es_type
    extract_logger.info("Extracting %s %s records for %s" %(dir_name, model.es_index, date))
    session = Session()
    try:
        q = model.extract(date)
        results = [{'index': model.es_index,
                'type': model.es_type,
                'body': serialize(model.schema, obj),
                'id':getattr(obj, model.es_id)} for obj in q]

        extract_logger.info("Extract successful")
        return results

    except Exception as e:
        extract_logger.info("Error extracting %s data for %s" % (model.es_index, date))
        extract_logger.error(e)
