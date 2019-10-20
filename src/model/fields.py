""" Tables for movie cateogry fields """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.model import db
from src.model import common


class MovieColor(db.ModelBase):
    """ Movie color """
    __tablename__ = 'movie_colors'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Movie color text
    name = Column(String(31), nullable=False, unique=True)

    #: Movie relationship
    movies = relationship('Movie', back_populates='movie_color')

    def __repr__(self):
        return '<MovieColor(name="%s")>' % self.name

    def __str__(self):
        return self.name


class Country(db.ModelBase):
    """ Country """
    __tablename__ = 'country'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Country name
    name = Column(String(31), nullable=False, unique=True)

    #: Movie relationship
    movies = relationship('Movie', back_populates='country')

    def __repr__(self):
        return '<Country(name="%s")>' % self.name

    def __str__(self):
        return self.name


class Language(db.ModelBase):
    """ Movie Language """
    __tablename__ = 'language'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Language name
    name = Column(String(31), nullable=False, unique=True)

    #: Movie relationship
    movies = relationship('Movie', back_populates='language')

    def __repr__(self):
        return '<Language(name="%s")>' % self.name

    def __str__(self):
        return self.name


class ContentRating(db.ModelBase):
    """ Movie content rating """
    __tablename__ = 'content_rating'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Rating name
    name = Column(String(31), nullable=False, unique=True)

    #: Movie relationship
    movies = relationship('Movie', back_populates='content_rating')

    def __repr__(self):
        return '<Content Rating(name="%s")>' % self.name

    def __str__(self):
        return self.name


class Genre(db.ModelBase):
    """ Movie genre """
    __tablename__ = 'genre'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Genre name
    name = Column(String(31), nullable=False, unique=True)

    movies = relationship(
        'Movie', secondary=common.movie_genres, back_populates='genres'
    )
