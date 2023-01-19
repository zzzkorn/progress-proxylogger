import threading
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

from common.variables import MAX_PACKAGE_LENGTH
from imitation.variables import POINT_RESPONSE
from imitation.variables import POINTS
from imitation.variables import SERVER_REGISTRATION_RESPONSE


def receive_messages(client: socket):
    print(len(POINTS))
    for _ in range(len(POINTS)):
        reply = client.recv(MAX_PACKAGE_LENGTH)
        print(reply)
        client.send(POINT_RESPONSE)


class ImitationServer(threading.Thread):
    def __init_socket(self, address, number_of_clients):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(number_of_clients)

    def __init__(self, address, number_of_clients):
        self.sock = None
        self.__init_socket(address, number_of_clients)
        super().__init__()

    def run(self):
        while True:
            client_sock, _ = self.sock.accept()
            print(_)
            try:
                client_sock.recv(MAX_PACKAGE_LENGTH)
                client_sock.send(SERVER_REGISTRATION_RESPONSE)
                client_sock.recv(MAX_PACKAGE_LENGTH)
                receive_messages(client_sock)
            finally:
                client_sock.close()


if __name__ == "__main__":
    imitation = ImitationServer(
        ("127.0.0.1", 50101),
        # ("185.60.134.234", 50101),
        # ("193.232.47.4", 40005),
        1,
    )
    imitation.start()
