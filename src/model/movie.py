""" Top level models for movie records and stats

Unnormalized movie fields:
    director_name, director_facebook_likes,
    actor_1_name, actor_1_facebook_likes,
    actor_2_name, actor_2_facebook_likes,
    actor_3_name, actor_3_facebook_likes,

Normalized movie fields:
    aspect_ratio, budget, cast_facebook_likes, color, content_rating, country,
    duration, facenumber_in_poster, genres, gross, imdb_id, imdb_score,
    language, movie_facebook_likes, movie_title, num_critic_for_reviews,
    num_voted_users, num_user_for_reviews, plot_keywords, title_year
"""
from sqlalchemy import (
    Column, ForeignKey, Integer, String, UniqueConstraint, Float
)
from sqlalchemy.orm import relationship

from src.model import db
from src.model import common
import src.model.fields
import src.model.person


class Movie(db.ModelBase):
    """ Movie Model """
    __tablename__ = 'movie'

    # Identification fields
    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Title to movie
    movie_title = Column(String(250), nullable=False)

    #: Title year (note: empty year should be treated as empty string)
    title_year = Column(String(16), nullable=False)

    # Stats fields
    #: Film aspect ratio
    aspect_ratio = Column(Float, nullable=True)

    #: Filming budget
    budget = Column(Float, nullable=True)

    #: Total number of facebook likes for all cast
    cast_facebook_likes = Column(Integer, nullable=True)

    #: Duration of a movie
    duration = Column(Integer, nullable=True)

    #: Number of faces in poster
    facenum = Column(Integer, nullable=True)

    #: Gross revenue
    gross = Column(Float, nullable=True)

    #: IMDB id
    imdb_id = Column(String(32), nullable=True)

    #: IMDB score
    imdb_score = Column(Float, nullable=True)

    #: Number of facebook likes for given movie
    movie_facebook_likes = Column(Integer, nullable=True)

    #: Critic number for reviews
    num_critic_for_reviews = Column(Integer, nullable=True)

    #: Number of users for reviews
    num_user_for_reviews = Column(Integer, nullable=True)

    #: Number of voted users
    num_voted_users = Column(Integer, nullable=True)

    # Relations
    #: Foreign key to content rating
    content_rating_pk = Column(Integer, ForeignKey('content_rating.pk'))
    content_rating = relationship('ContentRating', back_populates='movies')

    #: Foreign key to country
    country_pk = Column(Integer, ForeignKey('country.pk'))
    country = relationship('Country', back_populates='movies')

    #: Foreign key to language
    language_pk = Column(Integer, ForeignKey('language.pk'))
    language = relationship('Language', back_populates='movies')

    #: Foreign key to movie color
    movie_color_pk = Column(Integer, ForeignKey('movie_colors.pk'))
    movie_color = relationship('MovieColor', back_populates='movies')

    #: Foreign key to director person
    director_pk = Column(Integer, ForeignKey('person.pk'))
    director = relationship('Person', back_populates='directed_movies')

    #: Genres relation
    genres = relationship(
        'Genre', secondary=common.movie_genres, back_populates='movies'
    )

    #: Keywords relation
    keywords = relationship(
        'Keyword', secondary=common.movie_keywords, back_populates='movies'
    )

    #: Actors relation
    actors = relationship(
        'Person', secondary=common.movie_actors, back_populates='acted_movies'
    )

    #: Movies are uniquely identified by title and year
    UniqueConstraint('movie_title', 'title_year')

    def __repr__(self):
        return '<Movie(title="%s"; year="%s")>' % (
            self.movie_title, self.title_year
        )

    def __str__(self):
        return '%s (%s)' % (self.movie_title, self.title_year)
