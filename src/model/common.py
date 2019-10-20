""" Common dependencies for models """
from sqlalchemy import Column, Table, ForeignKey

from src.model import db


#: Many-many table for movies to genres
movie_genres = Table(
    'movie_genres', db.ModelBase.metadata,
    Column('movie_pk', ForeignKey('movie.pk'), primary_key=True),
    Column('genre_pk', ForeignKey('genre.pk'), primary_key=True)
)

#: Many-many table for movies to keywords
movie_keywords = Table(
    'movie_keywiards', db.ModelBase.metadata,
    Column('movie_pk', ForeignKey('movie.pk'), primary_key=True),
    Column('keyword_pk', ForeignKey('keyword.pk'), primary_key=True)
)
