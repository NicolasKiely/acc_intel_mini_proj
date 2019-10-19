""" Main file setting up model configuration

"""
import sqlalchemy
import os


class EngineWrapper(object):
    """ Manages SQLAlchemy engine and configuration """
    _engine_config_str = None
    _engine = None

    @classmethod
    def get_config_str(cls) -> str:
        return os.environ.get(
            cls.get_environ_db_connection_key(),
            cls.get_environ_db_connection_key()
        )

    @classmethod
    def get_engine(cls):
        """ Returns sqlalchemy engine """
        if cls._engine is None:
            cls._engine = sqlalchemy.create_engine(cls._engine_config_str)
        return cls._engine

    @staticmethod
    def get_default_db_connection_str() -> str:
        """ Default db connection """
        return 'sqlite:///data/db.sqlite'

    @staticmethod
    def get_environ_db_connection_key() -> str:
        """ Environment db connection key name """
        return 'DB_CONNECTION'
