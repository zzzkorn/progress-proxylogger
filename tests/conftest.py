from collections import OrderedDict
from pprint import pprint

import pytest
from decouple import AutoConfig
from decouple import RepositoryEnv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from conf import Config
from core.logger import LoggerCore
from database.logger import Base as LogBase
from tests.generator import generator


class TestConfig(Config):
    class TestAutoConfig(AutoConfig):
        SUPPORTED = OrderedDict([(".env-test", RepositoryEnv)])

    config = TestAutoConfig()


@pytest.fixture(scope="session", autouse=True)
def cfg():
    return TestConfig()


@pytest.fixture(scope="session", autouse=True)
def log_core():
    log_core = LoggerCore()
    return log_core


@pytest.fixture(scope="session", autouse=True)
def log_engine(cfg):
    engine = create_engine(
        cfg.database_engine,
        echo=False,
        pool_recycle=7200,
    )
    LogBase.metadata.drop_all(engine)
    LogBase.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session", autouse=True)
def log_session(log_engine):
    log_session = Session(log_engine)
    yield log_session
    log_session.close()


@pytest.fixture(scope="session", autouse=True)
def generate_objects(log_session):
    generator(log_session)


if __name__ == "__main__":
    config = TestConfig()
    pprint(config.__dict__)
