import logging
import pandas as pd
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

        # Build db
        engine = src.model.db.EngineWrapper.get_engine()
        src.model.db.ModelBase.metadata.create_all(engine)

        session = src.model.db.EngineWrapper.get_session()
        process_movie_colors(session, data)


def process_movie_colors(session, data):
    """ Processes list of unique colors in database """
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