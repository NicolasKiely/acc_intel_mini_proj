""" Main file setting up model configuration """
import logging
import os
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm


logger = logging.getLogger(__name__)

#: Base class for models
ModelBase = sqlalchemy.ext.declarative.declarative_base()


class EngineWrapper(object):
    """ Manages SQLAlchemy engine and configuration """
    _engine = None
    _session_factory = None

    @classmethod
    def get_config_str(cls) -> str:
        return os.environ.get(
            'DB_CONNECTION', 'sqlite:///data/db.sqlite'
        )

    @classmethod
    def get_engine(cls):
        """ Returns sqlalchemy engine """
        if cls._engine is None:
            logger.info('Connecting to database')
            cls._engine = sqlalchemy.create_engine(cls.get_config_str())
        return cls._engine

    @classmethod
    def get_session(cls):
        """ Returns new sqlalchemy session """
        if cls._session_factory is None:
            cls._session_factory = sqlalchemy.orm.sessionmaker(
                bind=cls.get_engine()
            )

        return cls._session_factory()
