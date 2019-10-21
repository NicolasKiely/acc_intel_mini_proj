""" Tables around actors/directors """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.model import db
from src.model import common


class Person(db.ModelBase):
    """ Person, such as actor or director """
    __tablename__ = 'person'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Movie color text
    name = Column(String(31), nullable=False, unique=True)

    #: Facebook likes
    likes = Column(Integer, nullable=True)

    #: Movies this person has directed
    directed_movies = relationship('Movie', back_populates='director')

    #: Movies this person has acted in
    acted_movies = relationship(
        'Movie', secondary=common.movie_actors, back_populates='actors'
    )

    def __repr__(self):
        return '<Person(name="%s")>' % self.name

    def __str__(self):
        return self.name
