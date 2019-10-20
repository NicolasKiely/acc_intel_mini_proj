import logging
import pandas as pd
import sqlalchemy
from typing import List

import src.model.db
import src.model.movie
import src.utils
from src.view import cli_view

logger = logging.getLogger(__name__)


class LoadDataView(cli_view.CliView):
    """ Loads data into database """
    def get_cli_name(self) -> str:
        return 'load-data'

    def do_command(self, argv: List[str]):
        if len(argv) == 0:
            file_name = src.utils.get_default_dataset_filename()

        elif len(argv) == 1:
            file_name = argv[0]

        else:
            print('Usage: %s [file name]' % self.get_cli_name())
            return

        logger.info('Loading file "%s"' % file_name)
        data = src.utils.load_df_from_dataset(file_name)

        # Build db and get session
        engine = src.model.db.EngineWrapper.get_engine()
        src.model.db.ModelBase.metadata.create_all(engine)
        session = src.model.db.EngineWrapper.get_session()

        # Process movie fields
        process_movie_colors(session, data)

        # Process move record itself
        process_movie_records(session, data)


def process_movie_colors(session, data: pd.DataFrame):
    """ Adds list of unique colors in database from data input """
    movie_colors = data['color'].unique()
    for movie_color_raw in movie_colors:
        # Clean up color name
        if pd.isna(movie_color_raw):
            continue
        movie_color = movie_color_raw.strip().lower()

        # Check if record exists in db
        old_color_record = session.query(
            src.model.movie.MovieColor
        ).filter(
            src.model.movie.MovieColor.color == movie_color
        ).one_or_none()

        if old_color_record is None:
            logger.info('Creating new movie_color record "%s"' % movie_color)
            new_color_record = src.model.movie.MovieColor(color=movie_color)
            session.add(new_color_record)

    session.commit()


def process_movie_records(session, data: pd.DataFrame):
    """ Adds list of movie records to database from data input """
    # Lookup of movie record number by title+year
    movie_title_index = {}
    for i, record in data.iterrows():
        record_no = i+1

        # Get searchable title+year of movie record
        movie_title = record['movie_title'].strip()
        movie_title_l = movie_title.lower()
        movie_year = record['title_year']

        if pd.isna(movie_title_l):
            logger.warning(
                'Movie with no title on record #%s' % record_no
            )
            continue

        if pd.isna(movie_year):
            logger.warning(
                'Movie with no year on record #%s' % record_no
            )
            movie_year = ''

        else:
            movie_year = str(movie_year)

        movie_record_index = (movie_title_l, movie_year)

        if movie_record_index in movie_title_index:
            logger.warning(
                'Duplicate movie "%s" (#%s, #%s)' % (
                    movie_title, movie_title_index[movie_title_l], record_no
                )
            )
            continue

        else:
            # Mark movie by record number in dataframe
            movie_title_index[movie_title_l] = record_no

        # Check if record exists in db by name
        old_movie_record = session.query(
            src.model.movie.Movie
        ).filter(
            sqlalchemy.func.lower(src.model.movie.Movie.movie_title)
            == movie_title_l
        ).filter(
            src.model.movie.Movie.title_year == movie_year
        ).one_or_none()

        if old_movie_record is None:
            # No record; create
            logger.info('Creating new movie record "%s"' % movie_title)
            movie_record = src.model.movie.Movie(
                movie_title=movie_title, title_year=movie_year
            )
            session.add(movie_record)

        else:
            movie_record = old_movie_record

    session.commit()
