import argparse
import sys

from decouple import config

from common import IMITATION_DELAY
from common import MAX_CONNECTIONS
from database import LoggerDatabase
from imitation import Imitation
from proxy import Server

local_host = config("HOST", default="localhost", cast=str)
local_port = config("PORT", cast=int)
maximum_connections = config(
    "MAXIMUM_CONNECTIONS",
    default=MAX_CONNECTIONS,
    cast=int,
)
remote_host = config("REMOVE_HOST", cast=str)
remote_port = config("REMOVE_PORT", cast=int)
imitation_delay = config("IMITATION_DELAY", default=IMITATION_DELAY, cast=int)
database_engine = config(
    "DATABASE_ENGINE",
    cast=str,
    default="sqlite:///test_base.db3",
)


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="main",
        description="""Proxy сервер с логированием данных""",
        epilog="(c)zzzkorn",
    )

    parser.add_argument(
        "-t",
        "--type",
        choices=["proxy", "imitation"],
        default="proxy",
        type=str,
        help="Тип запускаемого сервера",
    )
    return parser


def main():

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    script_type = namespace.type

    if script_type == "imitation":
        imitation = Imitation(
            local_host,
            local_port,
            remote_host,
            remote_port,
            maximum_connections,
            imitation_delay,
        )
        imitation.start()

    else:
        database = LoggerDatabase(eng=database_engine, file_log=True)

        server = Server(
            local_host,
            local_port,
            remote_host,
            remote_port,
            maximum_connections,
            database,
        )
        server.run()


if __name__ == "__main__":
    main()
