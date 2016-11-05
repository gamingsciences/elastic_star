# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:42:10 2016

@author: ken
"""
import datetime
from dateutil.parser import parse
import pandas as pd
from conformed_dimensions.models import ZipCode


def create_geopoint(zip_code):
    try:
        zipcode_obj = ZipCode.objects.filter(zip_code=str(zip_code)[:5])[0]
        geo_point={}
        geo_point['lat'] = float(zipcode_obj.lat)
        geo_point['lon'] = float(zipcode_obj.lat)
    except:
        geo_point={}
        
    return geo_point

def create_full_name(first, last):
    return first + ' ' + last
    
def calculate_age(audit_date, born):
    if isinstance(audit_date, pd.tslib.Timestamp):
        audit_date = audit_date.date()
    elif isinstance(audit_date, str):
        audit_date = parse(audit_date).date()
    elif isinstance(audit_date, datetime.datetime):
        audit_date = audit_date.date()
    
    try: 
        birthday = born.replace(year=audit_date.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=audit_date.year, day=born.day-1)
    if birthday > audit_date:
        return audit_date.year - born.year - 1
    else:
        return audit_date.year - born.year

transform_funcs = {'geo_from_zip': create_geopoint,
                   'full_name': create_full_name,
                   'calc_age': calculate_age}


#------------------------ helper functions ------------------------------------
# Get data from a dictionary with position provided as a list
def getFromDict(dataDict, mapList):    
    for k in mapList: dataDict = dataDict[k]
    return dataDict

# Set a given data in a dictionary with position provided as a list
def setInDict(dataDict, mapList, value): 
    for k in mapList[:-1]: dataDict = dataDict[k]
    dataDict[mapList[-1]] = value
