import socket
import sys
import threading


class Server:
    def __init__(
        self,
        listen_host,
        listen_port,
        remove_host,
        remove_port,
        maximum_connections,
        database,
    ):
        # Параментры подключения
        self.host = listen_host
        self.port = listen_port
        self.remove_host = remove_host
        self.remove_port = remove_port
        self.maximum_connections = maximum_connections
        self.sock = None

        # База данных сервера
        self.database = database

    def init_socket(self):
        self.database.logger.info(
            f"Запущен сервер {self.host}:{self.port}. Если адрес не указан, "
            f"принимаются соединения с любых адресов."
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.maximum_connections)

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while True:
            try:
                client, client_address = self.sock.accept()
                self.database.logger.info(
                    f"Установлено соедение {self.host}:{self.port} с "
                    f"{client_address}"
                )
                self.process_client_message(client, client_address)
            except KeyboardInterrupt:
                self.sock.close()
                self.database.logger.info(
                    f"Соедение {self.host}: {self.port} прервано"
                )
                sys.exit(1)

    def process_client_message(self, client, client_address):
        message = client.recv(8192)
        self.database.insert_sent_packet(client_address[0], message)
        proxy = Proxy(
            client,
            message,
            client_address,
            self.remove_host,
            self.remove_port,
            self.database,
        )
        # proxy.daemon = True
        proxy.start()


class Proxy(threading.Thread):
    def __init__(
        self,
        client,
        message,
        address,
        remove_host,
        remove_port,
        database,
    ):
        self.client = client
        self.sock = None
        self.message = message
        self.address = address
        self.host = None
        self.port = None
        self.remove_host = remove_host
        self.remove_port = remove_port
        self.database = database
        super().__init__()

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.remove_host, self.remove_port))
        self.host, self.port = self.sock.getpeername()

    def run(self):
        try:
            self.init_socket()
            self.sock.send(self.message)
            while True:
                reply = self.sock.recv(8192)
                self.database.insert_received_packet(self.address[0], reply)
                if len(reply):
                    self.client.send(reply)
                else:
                    break

            self.sock.close()
            self.client.close()
        except socket.error:
            self.sock.close()
            self.client.close()
            self.database.insert_error(self.address[0], socket.error)
            sys.exit(1)
