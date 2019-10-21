import logging
from typing import List

from src.view import cli_view


logger = logging.getLogger(__name__)


class RankGenresView(cli_view.CliView):
    """ Lists top n=10 genres ranked by profitability """
    def get_cli_name(self) -> str:
        return 'rank-genre'

    def do_command(self, argv: List[str]):
        if len(argv) == 0:
            num_genres = 10

        elif len(argv) == 1:
            num_genres = int(argv[0])

        else:
            print('Usage: %s [num_genres]' % self.get_cli_name())
            return

        logger.info('Loading top %s genres' % num_genres)
