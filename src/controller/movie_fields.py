""" Controller for movie category fields """
import abc
from typing import Dict, List

from src.controller import action
import src.model.db
import src.model.movie


class AddMovieColors(action.ControllerAction):
    """ Action to add list of movie colors to db, if they don't exist """
    def execute(self, color_names: List[str]):
        """
        :param color_names: List of movie colors by name
        """
        session = self.get_session()
        for color_name in color_names:
            # Check if record exists in db
            old_color_record = session.query(
                src.model.movie.MovieColor
            ).filter(
                src.model.movie.MovieColor.color == color_name
            ).one_or_none()

            if old_color_record is None:
                self.logger.info(
                    'Creating new movie_color record "%s"' % color_name
                )
                new_color_record = src.model.movie.MovieColor(color=color_name)
                session.add(new_color_record)

        self.commit(session)

    @abc.abstractmethod
    def query(self, **kwargs):
        pass


class MovieColorIndexLookup(action.ControllerAction):
    """ Action for building lookup of movie color id by name

    Builds dictionary mapping lower case color name to color record pk
    """
    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self) -> Dict[str, int]:
        session = self.get_session()
        lookup = {}
        movie_colors = session.query(src.model.movie.MovieColor).all()
        for movie_color in movie_colors:
            lookup[movie_color.color.lower()] = movie_color.pk

        return lookup


class AddCountry(action.ControllerAction):
    """ Action to add list of counties to db, if they don't exist """
    def execute(self, country_names: List[str]):
        """
        :param country_names: List of country names
        """
        session = self.get_session()
        for country_name in country_names:
            # Check if record exists in db
            old_country_record = session.query(
                src.model.movie.Country
            ).filter(
                src.model.movie.Country.name == country_name
            ).one_or_none()

            if old_country_record is None:
                self.logger.info(
                    'Creating new country record "%s"' % country_name
                )
                new_country_record = src.model.movie.Country(name=country_name)
                session.add(new_country_record)

        self.commit(session)

    @abc.abstractmethod
    def query(self, **kwargs):
        pass


class CountryIndexLookup(action.ControllerAction):
    """ Action for building lookup of country id by name

    Builds dictionary mapping lower case country name to country record pk
    """
    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self) -> Dict[str, int]:
        session = self.get_session()
        return {
            country.name.lower(): country.pk
            for country in session.query(src.model.movie.Country).all()
        }
