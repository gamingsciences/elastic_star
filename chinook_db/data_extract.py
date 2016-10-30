# -*- coding: utf-8 -*-
"""
The data_extract program uses Sqlalchemy automap to reflect the target 
database.  Marshmallow is then used to serialize the data.

It is the first part in the ETL process for ElasticStar.

Created on Sat Feb 06 15:48:10 2016

@author: Lathropk
"""
from django.conf import settings
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
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

# Create the Marshmallow Schemas for each Base Class
# also add nested object schema logic. Be mindful of the order of these classes
# Nested schemas must come before the primary schema

class ArtistSchema(ModelSchema):
    class Meta:
        model = Artist


class AlbumSchema(ModelSchema):
    artist = fields.Nested(ArtistSchema, exclude=('ArtistId',
                                                  'album_collection'))
    class Meta:
        model = Album
        

class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer

        
class EmployeeSchema(ModelSchema):
    class Meta:
        model = Employee


class GenreSchema(ModelSchema):
    class Meta:
        model = Genre

        
class MediaTypeSchema(ModelSchema):
    class Meta:
        model = MediaType
 
       
class TrackSchema(ModelSchema):
    album = fields.Nested(AlbumSchema, exclude=('track_collection',
                                                'AlbumId'))
    genre = fields.Nested(GenreSchema, exclude=('track_collection',
                                                'GenreId'))
    mediatype = fields.Nested(MediaTypeSchema, exclude=('track_collection',
                                                        'MediaTypeId'))
    class Meta:
        model = Track


class InvoiceLineSchema(ModelSchema):
    track = fields.Nested(TrackSchema, exclude=('playlist_collection',
                                                'UnitPrice',
                                                'invoiceline_collection'))
    class Meta:
        model = InvoiceLine

        
class InvoiceSchema(ModelSchema):
    invoiceline_collection = fields.Nested(InvoiceLineSchema, many=True, 
                                           exclude=('invoice',))
    class Meta:
        model = Invoice


class PlaylistSchema(ModelSchema):
    class Meta:
        model = Playlist

# Create your schema objects

album_schema = AlbumSchema()
artist_schema = ArtistSchema()
customer_schema = CustomerSchema()
employee_schema = EmployeeSchema()
genre_schema = GenreSchema()
invoiceline_schema = InvoiceLineSchema()
invoice_schema = InvoiceSchema()
mediatype_schema = MediaTypeSchema()
playlist_schema = PlaylistSchema()
track_schema = TrackSchema()

def serialize(schema, obj):
    dump_data = schema.dump(obj).data
    
    return dump_data

