import abc
import logging


class ControllerAction(object):
    """ Base action class """
    def __init__(self, logger_name: str):
        """ Sets up action instance """
        self._logger = logging.getLogger(logger_name)

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
