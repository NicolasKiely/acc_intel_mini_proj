import abc
import logging
from typing import Optional


class ControllerAction(object):
    """ Base action class """
    def __init__(self, logger: Optional[logging.Logger]):
        """ Sets up action instance """
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

    @property
    def logger(self):
        return self.logger

    @abc.abstractmethod
    def query(self, **kwargs):
        """ Action logic that returns some results with no side effects """
        pass

    @abc.abstractmethod
    def execute(self, **kwargs):
        """ Action logic to enacts some change on application state """
        pass
