import abc
import sqlalchemy

from src.controller import action
import src.model.movie


class AddMovie(action.ControllerAction):
    """ Adds movie record if it doesn't exist, otherwise updates it """
    def execute(
            self, movie_title: str, title_year: str, color_pk: int,
            duration: int, movie_facebook_likes: int,
            num_critic_for_reviews: int
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
            self.logger.info('Creating new movie record "%s"' % movie_title)
            movie_record = src.model.movie.Movie(
                movie_title=movie_title, title_year=title_year
            )
            session.add(movie_record)

        else:
            movie_record = old_movie_record

        # Set movie color
        movie_record.movie_color_pk = color_pk

        # Set movie stats
        movie_record.duration = duration
        movie_record.movie_facebook_likes = movie_facebook_likes
        movie_record.num_critic_for_reviews = num_critic_for_reviews

        self.commit(session)

    @abc.abstractmethod
    def query(self, **kwargs):
        pass
