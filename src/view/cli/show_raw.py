import logging
from typing import List

from src import utils
from src.view import cli_view


logger = logging.getLogger(__name__)


class ShowRawView(cli_view.CliView):
    """ Displays raw data from input csv

    Takes optional argument for file to load, otherwise defaults to
    'data/movie_metadata.csv'.
    """
    def do_command(self, argv: List[str]):
        if len(argv) == 0:
            file_name = utils.get_default_dataset_filename()

        elif len(argv) == 1:
            file_name = argv[0]

        else:
            print('Usage: %s [file name]' % self.get_cli_name())
            return

        logger.info('Loading file "%s"' % file_name)
        df = utils.load_df_from_dataset(file_name)

        print(df.head(5))

    def get_cli_name(self) -> str:
        return 'show-raw'
