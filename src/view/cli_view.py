""" Base class for cli """
import abc
from typing import List


class CliView(abc.ABC):
    """ Base class for command line interface views """
    @abc.abstractmethod
    def get_cli_name(self) -> str:
        """ Returns name identified on command line """
        pass

    @abc.abstractmethod
    def do_command(self, argv: List[str]):
        """ Run command invoked from CLI, given args """
        pass
