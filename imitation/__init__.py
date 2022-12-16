import time

from common import ENCODING
from imitation.client import ImitationClientBase
from imitation.packet import PacketBase
from imitation.server import ImitationServerBase


class ServerResponse(PacketBase):
    def get_packet_bytes(self):
        return f"{time.ctime(time.time())} \n".encode(ENCODING)


class ClientRequest(PacketBase):
    def get_packet_bytes(self):
        return "time request".encode(ENCODING)


class ImitationServer(ImitationServerBase):

    response = ServerResponse()


class ImitationClient(ImitationClientBase):

    request = ClientRequest()


class Imitation:
    clients = []
    server = None

    def __init__(
        self,
        listen_host: str,
        listen_port: int,
        remote_host: str,
        remote_port: int,
        number_of_clients: int = 3,
        delay: float = 2,
    ):
        self.init_server(remote_host, remote_port, number_of_clients)
        self.init_clients(listen_host, listen_port, number_of_clients, delay)

    def init_server(self, host, port, number_of_clients):
        self.server = ImitationServer(host, port, number_of_clients)

    def init_clients(self, host, port, number_of_clients, delay):
        for _ in range(number_of_clients):
            imitation_client = ImitationClient(host, port, delay)
            self.clients.append(imitation_client)

    def start(self):
        self.server.start()
        for imitation_client in self.clients:
            imitation_client.start()
