import abc
import sqlalchemy
from typing import List

from src.controller import action
import src.model.movie
import src.model.fields


class AddMovie(action.ControllerAction):
    """ Adds movie record if it doesn't exist, otherwise updates it """
    def execute(
            self, movie_title: str, title_year: str, color_pk: int,
            content_rating_pk: int, country_pk: int, language_pk: int,
            aspect_ratio: float, budget: float, cast_facebook_likes: int,
            duration: int, facenum: int, gross: float, imdb_id: str,
            imdb_score: float, movie_facebook_likes: int,
            num_critic_for_reviews: int, num_user_for_reviews: int,
            num_voted_users: int
    ):
        session = self.get_session()

        # Check if record exists in db by name
        old_movie_record = session.query(
            src.model.movie.Movie
        ).filter(
            sqlalchemy.func.lower(src.model.movie.Movie.movie_title)
            == movie_title.lower()
        ).filter(
            src.model.movie.Movie.title_year == title_year
        ).one_or_none()

        if old_movie_record is None:
            # No record; create
            movie_record = src.model.movie.Movie(
                movie_title=movie_title, title_year=title_year
            )
            session.add(movie_record)

        else:
            movie_record = old_movie_record

        # Set movie category fields
        movie_record.content_rating_pk = content_rating_pk
        movie_record.country_pk = country_pk
        movie_record.language_pk = language_pk
        movie_record.movie_color_pk = color_pk

        # Set movie stats
        movie_record.aspect_ratio = aspect_ratio
        movie_record.budget = budget
        movie_record.cast_facebook_likes = cast_facebook_likes
        movie_record.duration = duration
        movie_record.facenum = facenum
        movie_record.gross = gross
        movie_record.imdb_id = imdb_id
        movie_record.imdb_score = imdb_score
        movie_record.movie_facebook_likes = movie_facebook_likes
        movie_record.num_critic_for_reviews = num_critic_for_reviews
        movie_record.num_user_for_reviews = num_user_for_reviews
        movie_record.num_voted_users = num_voted_users

        self.commit(session)

    @abc.abstractmethod
    def query(self, **kwargs):
        pass


class MovieLookupIndex(action.ControllerAction):
    """ Action to build lookup table of movie (title, year) tuple to id """
    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self):
        session = self.get_session()
        return {
            (record.movie_title.lower(), record.title_year): record.pk
            for record in session.query(src.model.movie.Movie).all()
        }


class AttachMovieGenre(action.ControllerAction):
    """ Attaches genres to movie. Records must exist in db. """
    def execute(self, movie_pk: int, genre_pks: List[int]):
        session = self.get_session()

        # Fetch movie record
        movie_record = session.query(
            src.model.movie.Movie
        ).filter(src.model.movie.Movie.pk == movie_pk).one()

        # Fetch genre records
        genre_records = session.query(
            src.model.fields.Genre
        ).filter(src.model.fields.Genre.pk.in_(genre_pks)).all()

        for genre_record in genre_records:
            if genre_record in movie_record.genres:
                continue
            movie_record.genres.append(genre_record)

        self.commit(session)

    @abc.abstractmethod
    def query(self, **kwargs):
        pass
