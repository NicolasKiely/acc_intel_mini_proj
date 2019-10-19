from typing import List

from src.view import cli_view


class HelpView(cli_view.CliView):
    """ Prints help message for a given cli.py command """
    def __init__(self):
        super().__init__()
        self._views = []

    @property
    def views(self) -> List[cli_view.CliView]:
        """ Returns list of views """
        return self._views

    @views.setter
    def views(self, views: List[cli_view.CliView]):
        """ Setter for list of views """
        self._views = views

    def get_cli_name(self) -> str:
        return 'help'

    def do_command(self, argv: List[str]):
        if len(argv) == 1:
            print()

        else:
            print('Use help <command> to get help on a command')
            print('Available commands:')
            for view in self.views:
                print('\t%s' % view.get_cli_name())
