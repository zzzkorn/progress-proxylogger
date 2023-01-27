from common.enums import ImitationType
from conf import Config
from imitation.client import ImitationClient
from imitation.server import ImitationServer


class Imitation:
    clients = []
    server = None

    def __init__(self, cfg: Config, imitation_type: ImitationType):
        if imitation_type == ImitationType.full:
            self.init_server(
                cfg.remote,
                cfg.maximum_connections,
            )
        self.init_clients(
            cfg.address,
            cfg.maximum_connections,
            cfg.imitation_imei_ids,
            cfg.imitation_delay,
        )

    def init_server(self, remote, number_of_clients):
        self.server = ImitationServer(remote, number_of_clients)

    def init_clients(self, address, max_connections, imei_ids, delay):
        number_of_clients = max_connections
        if max_connections > len(imei_ids):
            number_of_clients = len(imei_ids)
        for i in range(number_of_clients):
            imitation_client = ImitationClient(
                address,
                imei_ids[i],
                delay,
            )
            self.clients.append(imitation_client)

    def start(self):

        if self.server:
            self.server.start()

        for imitation_client in self.clients:
            imitation_client.start()
