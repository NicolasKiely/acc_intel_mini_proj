""" Views for ranking stats """
import logging
from typing import List

import src.controller.stats
from src.view import cli_view


logger = logging.getLogger(__name__)


def profit_map_to_sorted_list(profit_map, num_limit):
    """ Returns sorted descending list from profit map of names to values """
    return sorted(
        [(name, profit) for name, profit in profit_map.items()],
        key=lambda x: x[1],
        reverse=True
    )[:num_limit]


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

        # Get genre profitability
        logger.info('Loading top %s genres' % num_genres)
        genre_profit_map = src.controller.stats.GenreProfit(logger).query()

        # Convert to list
        genre_profit_list = profit_map_to_sorted_list(
            genre_profit_map, num_genres
        )

        print('Genre\tAverage Profit')
        print('-----\t--------------')
        for genre, profit in genre_profit_list:
            print('%s\t%s' % (genre, int(profit)))


class RankPersonnelView(cli_view.CliView):
    """ Lists top actors and directors """
    def get_cli_name(self) -> str:
        return 'rank-personnel'

    def do_command(self, argv: List[str]):
        if len(argv) == 0:
            num_persons = 10

        elif len(argv) == 1:
            num_persons = int(argv[0])

        else:
            print('Usage: %s [num_genres]' % self.get_cli_name())
            return

        logger.info('Loading top %s persons' % num_persons)
        person_profit_map = src.controller.stats.PersonProfit(logger).query()

        # Convert to list
        person_profit_list = profit_map_to_sorted_list(
            person_profit_map, num_persons
        )

        print('Name\tAverage Profit')
        print('----\t--------------')
        for name, profit in person_profit_list:
            print('%s\t%s' % (name, int(profit)))
