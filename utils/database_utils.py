# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 09:46:38 2016

@author: ken
"""
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces


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
