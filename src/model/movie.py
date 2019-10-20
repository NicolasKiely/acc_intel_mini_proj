""" Top level models for movie records and stats

Unnormalized movie fields:
    color, director_name, num_critic_for_reviews, duration,
    director_facebook_likes, actor_3_facebook_likes, actor_2_name,
    actor_1_facebook_likes, gross, genres, actor_1_name, movie_title,
    num_voted_users, cast_total_facebook_likes, actor_3_name,
    facenumber_in_poster, plot_keywords, movie_imdb_link, num_user_for_reviews,
    language, country, content_rating, budget, title_year,
    actor_2_facebook_likes, imdb_score, aspect_ratio, movie_facebook_likes
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.model import db


class Movie(db.ModelBase):
    """ Movie Model """
    __tablename__ = 'movies'

    #: Primary key
    pk = Column(Integer, primary_key=True, autoincrement=True)

    #: Foreign key to movie color
    movie_color_pk = Column(Integer, ForeignKey('movie_colors.pk'))

    #: Movie color relationship
    movie_color = relationship('MovieColor', back_populates='movies')


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
