# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:19:53 2016

@author: Lathropk
"""
import pytz
import pandas as pd
from django.conf import settings

local_tz = pytz.timezone(settings.TIME_ZONE)

def utc_to_local(utc_d):
    utc_dt = pd.Timestamp(utc_d)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt
    
def local_to_utc(local_d):
    local_dt = pd.Timestamp(local_d)
    utc_dt = local_dt.replace(tzinfo=local_tz).astimezone(pytz.utc)
    return utc_dt
