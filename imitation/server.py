import threading
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

from common import MAX_PACKAGE_LENGTH


class ImitationServerBase(threading.Thread):
    def __init_socket(self, host, port, number_of_clients):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(number_of_clients)

    def __init__(self, host, port, number_of_clients):
        self.sock = None
        self.__init_socket(host, port, number_of_clients)
        super().__init__()

    @property
    def response(self):
        raise NotImplementedError

    def run(self):
        while True:
            client_sock, _ = self.sock.accept()
            try:
                client_sock.recv(MAX_PACKAGE_LENGTH)
                client_sock.send(self.response())
            finally:
                client_sock.close()
