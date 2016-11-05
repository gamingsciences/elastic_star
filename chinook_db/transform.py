# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:03:32 2016

@author: ken
"""
import os
import jsoncfg
from utils.transform_utils import create_geopoint, create_full_name, \
                                  getFromDict, setInDict


config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'transform_cfg.json')
config = jsoncfg.load_config(config_file)

transform_funcs = {'geo_from_zip': create_geopoint,
                   'full_name': create_full_name}

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
    