import socket
import sys
import threading

from common.conf import Config
from database import LoggerDatabase


class Server:
    def __init__(
        self,
        cfg: Config,
        database: LoggerDatabase,
    ):
        self.config = cfg
        self.address = cfg.address
        self.maximum_connections = cfg.maximum_connections
        self.max_package_length = cfg.max_package_length
        self.sock = None
        self.database = database

    def init_socket(self):
        self.database.logger.info(
            f"Запущен сервер {self.address}. Если адрес не указан, "
            f"принимаются соединения с любых адресов."
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.sock.listen(self.maximum_connections)

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while True:
            try:
                client, client_address = self.sock.accept()
                self.database.logger.info(
                    f"Установлено соедение {self.address} с "
                    f"{client_address}"
                )
                self.process_client_message(client, client_address[0])
            except KeyboardInterrupt:
                self.sock.close()
                self.database.logger.info(f"Соедение {self.address} прервано")
                sys.exit(1)

    def process_client_message(self, client, device_address):
        message = client.recv(self.max_package_length)
        self.database.insert_sent_packet(device_address, message)
        proxy = Proxy(
            client,
            message,
            device_address,
            self.config,
            self.database,
        )
        # proxy.daemon = True
        proxy.start()


class Proxy(threading.Thread):
    def __init__(
        self,
        client,
        message,
        device_address,
        cfg: Config,
        database: LoggerDatabase,
    ):
        self.client = client
        self.sock = None
        self.message = message
        self.device_address = device_address
        self.remote = cfg.remote
        self.max_package_length = cfg.max_package_length
        self.database = database
        super().__init__()

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.remote)

    def run(self):
        try:
            self.init_socket()
            self.sock.send(self.message)
            while True:
                reply = self.sock.recv(self.max_package_length)
                if len(reply):
                    self.database.insert_received_packet(
                        self.device_address,
                        reply,
                    )
                    self.client.send(reply)
                else:
                    break

            self.sock.close()
            self.client.close()

        except socket.error as e:
            self.database.insert_error(self.device_address, e)

        finally:
            self.sock.close()
            self.client.close()
            sys.exit(1)
