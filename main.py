from decouple import config

from common import LoggerDatabase
from common import Server

local_host = config("HOST", default="localhost", cast=str)
local_port = config("PORT", cast=int)
maximum_connections = config("MAXIMUM_CONNECTIONS", default=6, cast=int)
remote_host = config("REMOVE_HOST", cast=str)
remote_port = config("REMOVE_PORT", cast=int)
database_engine = config(
    "DATABASE_ENGINE",
    cast=str,
    default="sqlite:///test_base.db3",
)


def main():

    database = LoggerDatabase(
        engine=database_engine,
        file_log=True,
    )

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
