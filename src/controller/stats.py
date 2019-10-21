""" Stats-related queries """
import abc
from typing import Dict

from src.controller import action
import src.model.fields


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
                if movie_record.gross is None or movie_record.budget is None:
                    continue

                num_movies += 1
                total_profit += (movie_record.gross - movie_record.budget)

            if num_movies > 0:
                genre_values[genre_record.name] = total_profit / num_movies

        return genre_values
