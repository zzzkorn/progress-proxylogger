import argparse
import sys

from common.conf import Config
from database import LoggerDatabase
from decoder import Decoder
from imitation import Imitation
from proxy import Server


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="main",
        description="""Proxy сервер с логированием данных""",
        epilog="(c)zzzkorn",
    )

    parser.add_argument(
        "-t",
        "--type",
        choices=["proxy", "imitation", "decode"],
        default="proxy",
        type=str,
        help="Тип запускаемого сервера",
    )
    return parser


def main():

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    script_type = namespace.type

    cfg = Config()

    if script_type == "imitation":
        imitation = Imitation(cfg)
        imitation.start()

    elif script_type == "decode":
        database = LoggerDatabase(cfg)
        decoder = Decoder(database)
        decoder.run()

    else:
        database = LoggerDatabase(cfg)
        server = Server(cfg, database)
        server.run()


if __name__ == "__main__":
    main()
