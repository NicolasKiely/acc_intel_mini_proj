import abc
import logging


class ControllerAction(object):
    """ Base action class """
    def __init__(self, logger_name: str):
        """ Sets up action instance """
        self._logger = logging.getLogger(logger_name)

    @abc.abstractmethod
    def query(self, **kwargs):
        """ Returns some results with no side effects """
        pass

    @abc.abstractmethod
    def execute(self, **kwargs):
        """ Enacts some change on application state """
