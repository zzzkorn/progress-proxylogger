from collections import OrderedDict
from pprint import pprint
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

import pytest
from decouple import AutoConfig
from decouple import RepositoryEnv

from common.conf import Config
from common.variables import MAX_CONNECTIONS
from common.variables import TEST_SERVER_PORT


class TestConfig(Config):
    class TestAutoConfig(AutoConfig):
        SUPPORTED = OrderedDict([(".env-test", RepositoryEnv)])

    config = TestAutoConfig()


@pytest.fixture(scope="session", autouse=True)
def cfg():
    return TestConfig()


@pytest.fixture(scope="session", autouse=True)
def server_port():
    return TEST_SERVER_PORT


@pytest.fixture(scope="session", autouse=True)
def sever(server_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", server_port))
    sock.listen(MAX_CONNECTIONS)
    yield sock
    sock.close()


if __name__ == "__main__":
    config = TestConfig()
    pprint(config.__dict__)
