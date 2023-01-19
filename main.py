import argparse
import sys

from common.conf import Config
from common.enums import ImitationType
from imitation import Imitation
from proxy import Server


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="main",
        description="""Proxy сервер с логированием данных""",
        epilog="(c)Pavel Evseev",
    )

    parser.add_argument(
        "-t",
        "--type",
        choices=[
            "proxy",
            "client_imitation",
            "full_imitation",
            "decode",
        ],
        default="proxy",
        type=str,
        help=(
            "Тип запускаемого сервера:\n"
            "proxy - работа прокси сервера\n"
            "client_imitation - имитация работы клиентов (при запуске прокси "
            "сервера)\n"
            "full_imitation - полная имитация (при запуске прокси сервера)\n"
            "decode - парсинг принятых пакетов\n"
        ),
    )
    return parser


def main():

    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    script_type = namespace.type

    cfg = Config()

    if script_type in {"client_imitation", "full_imitation"}:
        imitation_type = {
            "client_imitation": ImitationType.client,
            "full_imitation": ImitationType.full,
        }[script_type]
        imitation = Imitation(cfg, imitation_type)
        imitation.start()

    elif script_type == "decode":
        # database = LoggerDatabase(cfg)
        # decoder = Decoder(database)
        # decoder.run()
        pass

    else:
        server = Server(cfg)
        server.run()


if __name__ == "__main__":
    main()
