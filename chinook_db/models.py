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
import types
from sqlalchemy import func
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

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
session = Session()
# some of the reflected tables don't generate a Base class like PlaylistTrack
# usually they are tables that don't have a primary key and are many-to-many
# tables.

#---------------------------Schemas---------------------------------------------
# Create the Marshmallow Schemas for each Base Class
# also add nested object schema logic. Be mindful of the order of these classes,
# Nested schemas must come before the primary schema

class ArtistSchema(ModelSchema):
    class Meta:
        model = Base.classes.Artist


class AlbumSchema(ModelSchema):
    artist = fields.Nested(ArtistSchema, exclude=('ArtistId',
                                                  'album_collection'))
    class Meta:
        model = Base.classes.Album


class CustomerSchema(ModelSchema):
    class Meta:
        model = Base.classes.Customer


class EmployeeSchema(ModelSchema):
    class Meta:
        model = Base.classes.Employee


class GenreSchema(ModelSchema):
    class Meta:
        model = Base.classes.Genre


class MediaTypeSchema(ModelSchema):
    class Meta:
        model = Base.classes.MediaType


class TrackSchema(ModelSchema):
    album = fields.Nested(AlbumSchema, exclude=('track_collection',
                                                'AlbumId'))
    genre = fields.Nested(GenreSchema, exclude=('track_collection',
                                                'GenreId'))
    mediatype = fields.Nested(MediaTypeSchema, exclude=('track_collection',
                                                        'MediaTypeId'))
    class Meta:
        model = Base.classes.Track


class InvoiceSchema(ModelSchema):
    customer = fields.Nested(CustomerSchema, exclude=('playlist_collection',
                                                'UnitPrice',
                                                'invoiceline_collection',
                                                'invoice_collection'))

    class Meta:
        model = Base.classes.Invoice
        exclude = ('invoiceline_collection',)


class InvoiceLineSchema(ModelSchema):
    track = fields.Nested(TrackSchema, exclude=('CustomerId',
                                                'invoiceline_collection',
                                                'playlist_collection'))

    invoice = fields.Nested(InvoiceSchema, only=('customer',
                                                 'InvoiceDate',
                                                 'InvoiceId'))

    class Meta:
        model = Base.classes.InvoiceLine


class PlaylistSchema(ModelSchema):
    class Meta:
        model = Base.classes.Playlist

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


#---------------------------EsModels--------------------------------------------

class EsModel:
    '''ElastiStar Model class
    '''

    def __init__(self,
                 base_model,
                 schema,
                 es_index='',
                 es_type='',
                 es_id='',
                 transforms=[],
                 date_field=None,
                 es_date_field=''
                 ):
        self.base_model = base_model
        self.schema = schema
        self.transforms = transforms
        self.es_index = es_index
        self.es_type = es_type
        self.es_id = es_id
        self.date_field = date_field,
        self.es_date_field = es_date_field


# Album Model-------------------------------------------------------------------
album = EsModel(base_model = Base.classes.Album,
                schema = album_schema,
                transforms = [],
                es_index = 'album',
                es_type = 'album',
                es_id = Base.classes.Album.AlbumId)

# Artist Model------------------------------------------------------------------
artist = EsModel(base_model = Base.classes.Artist,
                schema = artist_schema,
                transforms = [],
                es_index = 'artist',
                es_type = 'artist',
                es_id = Base.classes.Artist.ArtistId)

# Customer Model----------------------------------------------------------------
customer = EsModel(base_model = Base.classes.Customer,
                schema = customer_schema,
                transforms = [],
                es_index = 'customer',
                es_type = 'customer',
                es_id = Base.classes.Customer.CustomerId)

# Employee Model----------------------------------------------------------------
employee = EsModel(base_model = Base.classes.Employee,
                schema = employee_schema,
                transforms = [],
                es_index = 'employee',
                es_type = 'employee',
                es_id = Base.classes.Employee.EmployeeId)

# Genre Model-------------------------------------------------------------------
genre = EsModel(base_model = Base.classes.Genre,
                schema = genre_schema,
                transforms = [],
                es_index = 'genre',
                es_type = 'genre',
                es_id = Base.classes.Genre.GenreId)

# Invoice Model-----------------------------------------------------------------
invoice = EsModel(base_model = Base.classes.Invoice,
                schema = invoice_schema,
                transforms = [
                    {
                        "transform_func": "geo_from_zip",
                        "data_fields": {
                                        "zip_code": ["customer", "PostalCode"]
                                     },
                        "target_field_name": ["customer", "geo_point"]
                    },
                    {
                        "transform_func": "full_name",
                        "data_fields": {
                                        "first": ["customer", "FirstName"],
                                        "last": ["customer", "LastName"]
                                     },
                        "target_field_name": ["customer", "FullName"]
                    }
                ],
                es_index = 'chinook_invoice',
                es_type = 'invoice',
                es_id = 'InvoiceId',
                date_field = Base.classes.Invoice.InvoiceDate,
                es_date_field='InvoiceDate')

def invoice_ext_func(self, date):
    return session.query(self.base_model).filter(func.date(self.base_model.InvoiceDate) == date)

invoice.extract = types.MethodType(invoice_ext_func, invoice)

# InvoiceLine Model-------------------------------------------------------------
invoice_line = EsModel(base_model = Base.classes.InvoiceLine,
                schema = invoiceline_schema,
                transforms = [
                    {
                        "transform_func": "geo_from_zip",
                        "data_fields": {
                                        "zip_code": ["customer", "PostalCode"]
                                     },
                        "target_field_name": ["customer", "geo_point"]
                    },
                    {
                        "transform_func": "full_name",
                        "data_fields": {
                                        "first": ["customer", "FirstName"],
                                        "last": ["customer", "LastName"]
                                     },
                        "target_field_name": ["customer", "FullName"]
                    }
                ],
                es_index = 'invoiceline',
                es_type = 'invoiceline',
                es_id = 'InvoiceLineId',
                date_field = Base.classes.Invoice.InvoiceDate,
                es_date_field='invoice.InvoiceDate')

def invoiceline_ext_func(self, date):
    return session.query(self.base_model).join(Base.classes.Invoice)\
                .filter(func.date(Base.classes.Invoice.InvoiceDate) == date)

invoice_line.extract = types.MethodType(invoiceline_ext_func, invoice_line)

# MediaType Model---------------------------------------------------------------
media_type = EsModel(base_model = Base.classes.MediaType,
                schema = mediatype_schema,
                transforms = [],
                es_index = 'media_type',
                es_type = 'media_type',
                es_id = Base.classes.MediaType.MediaTypeId)

# PlayList Model----------------------------------------------------------------
playlist = EsModel(base_model = Base.classes.Playlist,
                schema = playlist_schema)

# Track Model-------------------------------------------------------------------
track = EsModel(base_model = Base.classes.Track,
                schema = track_schema,
                transforms = [],
                es_index = 'track',
                es_type = 'track',
                es_id = Base.classes.Track.TrackId)
