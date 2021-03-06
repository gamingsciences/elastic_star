# -*- coding: utf-8 -*-
"""
Trandsform functions for ElasticStar.  Uses the transform field in the
EsModel to determine what transforms are performed on which fields of the json
document created in the data extract.  Uses the helper functions getFromDict
and setInDict.

Created on Fri Nov  4 17:03:32 2016

@author: ken
"""
import os
from utils.transform_utils import transform_funcs, getFromDict, setInDict
from utils.loggers import TransformLogger

logger = TransformLogger()
transform_logger = logger.myLogger()


def transform(model, doc_dict):
    for transform in model.transforms:
        data_fields = transform['data_fields']
        for key, val in data_fields.items():
            data_fields[key] = getFromDict(doc_dict['body'], val)

        trans_func = transform_funcs[transform['transform_func']]

        new_data = trans_func(**data_fields)

        setInDict(doc_dict['body'], transform['target_field_name'], new_data)

    return doc_dict

def batch_transform(model, date, doc_list):
    transformed_docs = []
    dir_name = os.path.dirname(os.path.abspath(__file__)
    transform_logger.info("Transforming %s records for %s" %(dir_name, date))
    for doc in doc_list:
        try:
            transformed_docs.append(transform(model, doc))
        except Exception as e:
            transform_logger.info("Error transforming %s data for %s" % (dir_name, date))
            transform_logger.error(e, exec_info=True)

    return transformed_docs
