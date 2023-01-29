from collections import namedtuple
from pprint import pprint

from decouple import Csv
from decouple import config

from common.errors import ConfigError
from common.variables import DATABASE_ENGINE
from common.variables import FILE_LOG
from common.variables import IMITATION_DELAY
from common.variables import IMITATION_IMEI_IDS
from common.variables import MAX_CONNECTIONS
from common.variables import MAX_PACKAGE_LENGTH
from common.variables import SOCKET_TIMEOUT


class ProxyPorts(Csv):

    Ports = namedtuple("Ports", ["start", "end"])

    def __validate(self):
        if len(self.ports) != 2:
            raise ConfigError(
                "PROXY_PORT_RANGE",
                "Диапазон доступных портов должен состоять из 2 значений",
            )
        if self.ports[0] > self.ports[1]:
            raise ConfigError(
                "PROXY_PORT_RANGE",
                "Первый номер в диапазоне должен быть больше последнего",
            )

    def __call__(self, value):
        self.ports = super().__call__(value)
        self.__validate()
        return self.Ports(self.ports[0], self.ports[1])


def cast_as_address(gen):
    types = [str, int]
    res = []
    for i, el in enumerate(gen):
        res.append(types[i](el))
    return tuple(res)


class Config:

    config = config

    def _validate(self):
        pass

    def _read_cfg(self):

        self.address = self.config(
            "ADDRESS",
            cast=Csv(str, delimiter=":", post_process=cast_as_address),
        )
        self.remote = self.config(
            "REMOTE",
            cast=Csv(str, delimiter=":", post_process=cast_as_address),
        )

        self.maximum_connections = self.config(
            "MAX_CONNECTIONS",
            default=MAX_CONNECTIONS,
            cast=int,
        )
        self.max_package_length = self.config(
            "MAX_PACKAGE_LENGTH",
            default=MAX_PACKAGE_LENGTH,
            cast=int,
        )
        self.imitation_delay = self.config(
            "IMITATION_DELAY",
            default=IMITATION_DELAY,
            cast=float,
        )
        self.socket_timeout = self.config(
            "SOCKET_TIMEOUT",
            default=SOCKET_TIMEOUT,
            cast=float,
        )
        self.database_engine = self.config(
            "DATABASE_ENGINE",
            default=DATABASE_ENGINE,
            cast=str,
        )
        self.proxy_ports = self.config(
            "PROXY_PORT_RANGE",
            cast=ProxyPorts(int),
        )
        self.file_log = self.config("FILE_LOG", default=FILE_LOG, cast=bool)
        self.imitation_imei_ids = self.config(
            "IMITATION_IMEI_IDS",
            cast=Csv(int),
            default=IMITATION_IMEI_IDS,
        )

    def __init__(self):
        self._read_cfg()
        self._validate()


if __name__ == "__main__":
    cfg = Config()
    pprint(cfg.__dict__)
