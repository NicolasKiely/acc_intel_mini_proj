""" Miscellaneous utility functions """
import logging
import os
import pandas as pd


logger = logging.getLogger(__name__)


def load_df_from_dataset(file_name: str) -> pd.DataFrame:
    """ Loads cleaned dataframe from csv

    Fields with extra records get logged and dropped.
    """
    df = pd.read_csv(file_name)
    bad_column = None
    bad_column_name = None
    for column in df.columns:
        if not column.startswith('Unnamed:'):
            # Only care about unnamed columns
            continue

        column_id = column.split(':')[-1].strip()
        if column_id == '0':
            # Ignore unnamed column if it is the very first one (eg index)
            continue

        bad_column_name = column
        bad_column = df[column]
        logger.warning('Found suspicious column "%s"' % column)

    if bad_column is not None:
        # Drop records that have entries in trailing unnamed column
        bad_records = df[bad_column.notna()]
        for record in bad_records.iterrows():
            logger.warning('Skipping record: #%s' % record[0])

        df = df.drop(bad_records.index)
        df = df.drop(columns=[bad_column_name])

    return df


def get_default_dataset_filename() -> str:
    """ Returns default dataset file name """
    return os.environ.get('DATASET_NAME', 'data/movie_metadata.csv')


def nan_to_none(value, default=None):
    """ Casts numpy/pandas nan values to none, or some other default """
    if pd.isna(value):
        return default
    else:
        return value
