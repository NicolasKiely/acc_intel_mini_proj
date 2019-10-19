from typing import Dict, List

from src.view import cli_view


class HelpView(cli_view.CliView):
    """ Prints help message for a given cli.py command

    If given a command name as an argument, prints user help message for that
    command. Otherwise just prints usage and list of recognized commands.
    """
    def __init__(self):
        super().__init__()
        self._view_lookup = {}

    @property
    def view_lookup(self) -> Dict[str, cli_view.CliView]:
        """ Returns list of views """
        return self._view_lookup

    @view_lookup.setter
    def view_lookup(self, views: Dict[str, cli_view.CliView]):
        """ Setter for list of views """
        self._view_lookup = views

    def get_cli_name(self) -> str:
        return 'help'

    def do_command(self, argv: List[str]):
        if len(argv) == 1:
            command_name = argv[0]
            if command_name in self.view_lookup:
                print(self.view_lookup[command_name].__doc__.strip())

            else:
                print('Error, command "%s" not recognized' % command_name)

        else:
            print('Use help <command> to get help on a command')
            print('Available commands:')
            for view in self.view_lookup.values():
                print('\t%s' % view.get_cli_name())
