import logging
import pandas as pd
from typing import List

from src.view import cli_view


logger = logging.getLogger(__name__)


class ShowRawView(cli_view.CliView):
    """ Displays raw data from input csv

    Takes optional argument for file to load, otherwise defaults to
    'data/movie_metadata.csv'.
    """
    def do_command(self, argv: List[str]):
        if len(argv) == 0:
            file_name = self.get_default_filename()

        elif len(argv) == 1:
            file_name = argv[0]

        else:
            print('Usage: %s [file name]' % self.get_cli_name())
            return

        logger.info('Loading file "%s"' % file_name)
        df = load_df_from_dataset(file_name)

        print(df.head(5))

    def get_cli_name(self) -> str:
        return 'show-raw'

    @staticmethod
    def get_default_filename() -> str:
        return 'data/movie_metadata.csv'


def load_df_from_dataset(file_name: str) -> pd.DataFrame:
    """ Loads cleaned dataframe from csv

    Fields with extra records get logged and dropped
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
