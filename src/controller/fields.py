""" Controller for movie category fields """
import abc
from typing import Dict, List

from src.controller import action
import src.model.db
import src.model.fields


class AddMovieFieldBaseClass(action.ControllerAction):
    """ Base class for adding category fields """
    def execute_add(self, names: List[str], model_class, class_name: str):
        """
        :param names: List of names of records to add
        :param model_class: Model class
        :param class_name: Name of class to log
        """
        session = self.get_session()
        for name in names:
            # Check if record exists in db
            old_record = session.query(
                model_class
            ).filter(
                model_class.name == name
            ).one_or_none()

            if old_record is None:
                self.logger.info(
                    'Creating new %s record "%s"' % (class_name, name)
                )
                session.add(model_class(name=name))

        self.commit(session)

    @abc.abstractmethod
    def execute(self, **kwargs):
        pass

    def query(self, **kwargs):
        pass


class MovieFieldIndexLookup(action.ControllerAction):
    """ Base class for building lookup of record id by name

    Builds dictionary mapping lower case name to record pk
    """
    def query_index_lookup(self, model_class):
        session = self.get_session()
        return {
            record.name.lower(): record.pk
            for record in session.query(model_class).all()
        }

    @abc.abstractmethod
    def query(self, **kwargs):
        pass

    def execute(self, **kwargs):
        pass


class AddMovieColors(AddMovieFieldBaseClass):
    """ Action to add list of movie colors to db, if they don't exist """
    def execute(self, color_names: List[str]):
        self.execute_add(color_names, src.model.fields.MovieColor, 'moviecolor')


class MovieColorIndexLookup(MovieFieldIndexLookup):
    """ Action for building lookup of movie color id by name """
    def query(self) -> Dict[str, int]:
        return self.query_index_lookup(src.model.fields.MovieColor)


class AddCountries(AddMovieFieldBaseClass):
    """ Action to add list of counties to db, if they don't exist """
    def execute(self, country_names: List[str]):
        self.execute_add(country_names, src.model.fields.Country, 'country')


class CountryIndexLookup(MovieFieldIndexLookup):
    """ Action for building lookup of country id by name """
    def query(self) -> Dict[str, int]:
        return self.query_index_lookup(src.model.fields.Country)


class AddLanguages(AddMovieFieldBaseClass):
    """ Action to add list of languages to db, if they don't exist """
    def execute(self, language_names: List[str]):
        self.execute_add(language_names, src.model.fields.Language, 'language')


class LanguageIndexLookup(MovieFieldIndexLookup):
    """ Action for building lookup of language id by name """
    def query(self) -> Dict[str, int]:
        return self.query_index_lookup(src.model.fields.Language)


class AddContentRating(AddMovieFieldBaseClass):
    """ Action to add list of content ratings to db, if they don't exist """
    def execute(self, rating_names: List[str]):
        self.execute_add(rating_names, src.model.fields.ContentRating, 'rating')


class ContentRatingIndexLookup(MovieFieldIndexLookup):
    """ Action for building lookup of content rating id by name """
    def query(self) -> Dict[str, int]:
        return self.query_index_lookup(src.model.fields.ContentRating)


class AddGenres(AddMovieFieldBaseClass):
    """ Action to add list of genres to db, if they don't exist """
    def execute(self, genre_names: List[str]):
        self.execute_add(genre_names, src.model.fields.Genre, 'genre')
