# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 11:50:50 2016

@author: ken
"""
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .models import Album, Artist, Customer, Employee, Genre, \
                   Invoice, InvoiceLine, MediaType, Playlist, Track


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
    track = fields.Nested(TrackSchema, exclude=('CustomerId',))
    class Meta:
        model = InvoiceLine

        
class InvoiceSchema(ModelSchema):
    customer = fields.Nested(CustomerSchema, exclude=('playlist_collection',
                                                'UnitPrice',
                                                'invoiceline_collection'))
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
