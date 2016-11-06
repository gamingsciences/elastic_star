# -*- coding: utf-8 -*-
"""
Defines the Sqlalchemy models for the tables in the Chinook DB.

Created on Sun Oct 30 11:53:55 2016

@author: ken
"""

from django.conf import settings
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from utils.database_utils import _gen_relationship


engine = settings.CHINOOK_ENGINE
metadata = MetaData()
metadata.reflect(engine, only=['Album', 
                               'Artist',
                               'Customer',
                               'Employee',
                               'Genre',
                               'Invoice',
                               'InvoiceLine',
                               'MediaType',
                               'Playlist',
                               'PlaylistTrack',
                               'Track'])

Base = automap_base(metadata=metadata)
    
Base.prepare(generate_relationship=_gen_relationship)

Session = sessionmaker(bind=engine)

# some of the reflected tables don't generate a Base class like PlaylistTrack
# usually they are tables that don't have a primary key and are many-to-many 
# tables. 

Album = Base.classes.Album
Artist = Base.classes.Artist
Customer = Base.classes.Customer
Employee = Base.classes.Employee
Genre = Base.classes.Genre
Invoice = Base.classes.Invoice
InvoiceLine = Base.classes.InvoiceLine
MediaType = Base.classes.MediaType
Playlist = Base.classes.Playlist
Track = Base.classes.Track
