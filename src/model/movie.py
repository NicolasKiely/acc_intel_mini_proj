""" Top level models for movie records and stats

Unnormalized movie fields:
    director_name,
    director_facebook_likes, actor_3_facebook_likes, actor_2_name,
    actor_1_facebook_likes, genres, actor_1_name,
    actor_3_name,
    plot_keywords, movie_imdb_link,
    language, content_rating,
    actor_2_facebook_likes
    country

Normalized movie fields:
    aspect_ratio, budget, cast_facebook_likes, color, duration,
    facenumber_in_poster, gross, imdb_score, movie_facebook_likes, movie_title,
    num_critic_for_reviews, num_voted_users, num_user_for_reviews, title_year
"""
from sqlalchemy import (
    Column, ForeignKey, Integer, String, UniqueConstraint, Float
)
from sqlalchemy.orm import relationship

from src.model import db


class Movie(db.ModelBase):
    """ Movie Model """
    __tablename__ = 'movies'

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
    #: Foreign key to movie color
    movie_color_pk = Column(Integer, ForeignKey('movie_colors.pk'))

    #: Movie color relationship
    movie_color = relationship('MovieColor', back_populates='movies')

    #: Movies are uniquely identified by title and year
    UniqueConstraint('movie_title', 'title_year')


class MovieColor(db.ModelBase):
    """ Movie color """
    __tablename__ = 'movie_colors'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Movie color text
    color = Column(String(31), nullable=False, unique=True)

    #: Movie relationship
    movies = relationship('Movie', back_populates='movie_color')

    def __repr__(self):
        return '<MovieColor(color="%s")>' % self.color

    def __str__(self):
        return self.color
