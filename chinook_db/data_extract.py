# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 15:48:10 2016

@author: Lathropk
"""
from django.conf import settings
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


engine = settings.CHINOOK_ENGINE
metadata = MetaData()
metadata.reflect(engine, only=['Album', 
                               'Artist'])

Base = automap_base(metadata=metadata)
Base.prepare()

Session = sessionmaker(bind=engine)

Album = Base.classes.Album
Artist = Base.classes.Artist

def test_extract():
    session = Session()
    query = session.query(Album, Artist).join('ArtistId')
    session.close()
    
    return query.all()