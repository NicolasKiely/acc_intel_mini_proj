import logging
import pandas as pd
import re
from typing import List

import src.controller.movie
import src.controller.movie_colors
import src.model.db
import src.model.movie
import src.utils
from src.view import cli_view

logger = logging.getLogger(__name__)


# Regular expression for pulling out id from IMDB url
IMDB_URL_ID_RE = re.compile('title/tt(\d+)/')


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
        process_movie_colors(data)

        # Process move record itself
        process_movie_records(session, data)


def process_movie_colors(data: pd.DataFrame):
    """ Adds list of unique colors in database from data input """
    raw_movie_colors = data['color'].unique()
    movie_colors = []
    for raw_movie_color in raw_movie_colors:
        # Clean up color name
        if pd.isna(raw_movie_color):
            continue
        movie_color = raw_movie_color.strip().lower()
        movie_colors.append(movie_color)

    src.controller.movie_colors.AddMovieColors(logger).execute(
        color_names=movie_colors
    )


def process_movie_records(session, data: pd.DataFrame):
    """ Adds list of movie records to database from data input """
    # Lookup of movie record number by title+year
    movie_color_lookup = src.controller.movie_colors.MovieColorIndexLookup(
        logger
    ).query()
    movie_title_index = {}
    for i, record in data.iterrows():
        record_no = i+1

        if record_no % 500 == 0:
            print('Processing record #%s' % record_no)

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

        # Get movie color id
        raw_movie_color_name = record['color']
        if not pd.isna(raw_movie_color_name):
            movie_color_name = raw_movie_color_name.strip().lower()
            movie_color_pk = movie_color_lookup[movie_color_name]

        else:
            movie_color_pk = None

        # Get movie's imdb id
        imdb_link = record['movie_imdb_link']
        if imdb_link:
            search_results = IMDB_URL_ID_RE.search(imdb_link)
            if search_results is None:
                imdb_id = None
            else:
                imdb_id = search_results.group(1)
        else:
            imdb_id = None

        # Get movie's numerical stats
        aspect_ratio = src.utils.nan_to_none(record['aspect_ratio'])
        budget = src.utils.nan_to_none(record['budget'])
        cast_likes = src.utils.nan_to_none(record['cast_total_facebook_likes'])
        duration = src.utils.nan_to_none(record['duration'])
        facenum = src.utils.nan_to_none(record['facenumber_in_poster'])
        gross = src.utils.nan_to_none(record['gross'])
        imdb_score = src.utils.nan_to_none(record['imdb_score'])
        facebook_likes = src.utils.nan_to_none(record['movie_facebook_likes'])
        num_critic = src.utils.nan_to_none(record['num_critic_for_reviews'])
        num_user = src.utils.nan_to_none(record['num_user_for_reviews'])
        num_voted = src.utils.nan_to_none(record['num_voted_users'])

        # Add movie record. Manaully take over session and comitting
        src.controller.movie.AddMovie(
            logger=logger, session=session, commit_enabled=False
        ).execute(
            movie_title=movie_title, title_year=movie_year,
            color_pk=movie_color_pk, aspect_ratio=aspect_ratio, budget=budget,
            cast_facebook_likes=cast_likes, duration=duration, facenum=facenum,
            gross=gross, imdb_id=imdb_id, imdb_score=imdb_score,
            movie_facebook_likes=facebook_likes,
            num_critic_for_reviews=num_critic, num_user_for_reviews=num_user,
            num_voted_users=num_voted
        )

    session.commit()
