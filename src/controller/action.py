import abc
import logging
from typing import Optional

import src.model.db


class ControllerAction(object):
    """ Base action class """
    def __init__(
            self, logger: Optional[logging.Logger]=None, session=None,
            commit_enabled: Optional[bool]=True
    ):
        """ Sets up action instance
        :param logger: Optional logger of invoking view
        :param session: Optional session to use, persistent across action life
        :param commit_enabled: Whether or not committing is enabled
        """
        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self._session = session
        self._commit_enabled = commit_enabled

    @property
    def logger(self):
        return self._logger

    @abc.abstractmethod
    def query(self, **kwargs):
        """ Action logic that returns some results with no side effects """
        pass

    @abc.abstractmethod
    def execute(self, **kwargs):
        """ Action logic to enacts some change on application state """
        pass

    def get_session(self):
        """ Returns sqlalchemy session """
        if self._session is None:
            return src.model.db.EngineWrapper.get_session()
        else:
            return self._session

    def commit(self, session):
        """ Tries to commit db session, unless disabled """
        if self._commit_enabled:
            session.commit()
