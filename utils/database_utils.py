# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 09:46:38 2016

@author: ken
"""
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces
import csv
from conformed_dimensions.models import ZipCode


def _gen_relationship(base, direction, return_fn,
                                attrname, local_cls, referred_cls, **kw):
    if direction is interfaces.ONETOMANY:
        kw['cascade'] = 'all, delete-orphan'
        kw['passive_deletes'] = True
    # make use of the built-in function to actually return
    # the result.
    return generate_relationship(base, direction, return_fn,
                                 attrname, local_cls, referred_cls, **kw)
                                 
def serialize(schema, obj):
    dump_data = schema.dump(obj).data
    
    return dump_data
    
def load_zipcode_data(filename):
    with open(filename, 'r')as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            code = ZipCode(zip_code = row[1],
                           state_abrev = row[2],
                           lat = row[3],
                           lon = row[4],
                           city = row[5],
                           state = row[6])
            code.save()
