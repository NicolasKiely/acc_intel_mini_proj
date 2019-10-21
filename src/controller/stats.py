""" Stats-related queries """
import abc
from typing import Dict

from src.controller import action
import src.model.fields
import src.model.person


def get_moview_profit(movie_record):
    """ Computes profit from movie, or returns None if not applicable """
    if movie_record.gross is None or movie_record.budget is None:
        return None

    return movie_record.gross - movie_record.budget


class GenreProfit(action.ControllerAction):
    """ Return mapping of genres to profitablity """
    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self) -> Dict[str, float]:
        session = self.get_session()

        # Map of genre to profit
        genre_values = {}

        genre_records = session.query(src.model.fields.Genre).all()
        for genre_record in genre_records:
            total_profit = 0.0
            num_movies = 0
            for movie_record in genre_record.movies:
                movie_profit = get_moview_profit(movie_record)
                if movie_profit is None:
                    continue

                num_movies += 1
                total_profit += movie_profit

            if num_movies > 0:
                genre_values[genre_record.name] = total_profit / num_movies

        return genre_values


class PersonProfit(action.ControllerAction):
    """ Returns mapping of directors/actors to profitability """
    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self) -> Dict[str, float]:
        session = self.get_session()

        person_values = {}
        person_records = session.query(src.model.person.Person).all()
        for person_record in person_records:
            movie_pks_used = set()

            total_profit = 0.0
            num_movies = 0

            for acted_movie in person_record.acted_movies:
                if acted_movie.pk in movie_pks_used:
                    # Already processed movie
                    continue
                movie_pks_used.add(acted_movie.pk)

                movie_profit = get_moview_profit(acted_movie)
                if movie_profit is None:
                    continue
                num_movies += 1
                total_profit += movie_profit

            for directed_movie in person_record.directed_movies:
                if directed_movie.pk in movie_pks_used:
                    # Already processed movie
                    continue
                movie_pks_used.add(directed_movie.pk)

                movie_profit = get_moview_profit(directed_movie)
                if movie_profit is None:
                    continue
                num_movies += 1
                total_profit += movie_profit

            if num_movies > 0:
                person_values[person_record.name] = total_profit / num_movies

        return person_values
