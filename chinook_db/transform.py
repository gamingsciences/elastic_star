# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:03:32 2016

@author: ken
"""
import os
import jsoncfg
from utils.transform_utils import transform_funcs, getFromDict, setInDict
from .utils.loggers import ChinookTransformLogger

logger = TransformLogger()
transform_logger = logger.myLogger()


config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'transform_cfg.json')
config = jsoncfg.load_config(config_file)


def transform(doc_dict):
    transforms = []
    # get list of transforms for the doc_dict's index and type
    index = doc_dict["index"]
    type_ = doc_dict["type"]
    for idx in config.indexes:
        if idx.index() == index and idx.type() == type_:
            transforms = idx.transforms()
    
    for transform in transforms:
        data_fields = transform['data_fields']
        for key, val in data_fields.items():
            data_fields[key] = getFromDict(doc_dict['body'], val)
            
        trans_func = transform_funcs[transform['transform_func']]
        
        new_data = trans_func(**data_fields)
        
        setInDict(doc_dict['body'], transform['target_field_name'], new_data)
        
    return doc_dict
    
def batch_transform(date, doc_list):
    transformed_docs = []
    transform_logger.info("Transforming chinook invoice records for %s" %date )
    for doc in doc_list:
        try:
            transformed_docs.append(transform(doc))
        except Exception as e:
            transform_logger.info("Error extracting chinook invoice data for %s" % date)
            transform_logger.error(e, exec_info=True)
        
    return transformed_docs

