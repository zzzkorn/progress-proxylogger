# import time
#
# from common.conf import Config
# from common.variables import ENCODING
# from imitation.client import ImitationClientBase
# from imitation.packet import PacketBase
# from imitation.server import ImitationServerBase
#
#
# class ServerResponse(PacketBase):
#     def get_packet_bytes(self):
#         return f"{time.ctime(time.time())} \n".encode(ENCODING)
#
#
# class ClientRequest(PacketBase):
#     def get_packet_bytes(self):
#         return "time request".encode(ENCODING)
#
#
# class ImitationServer(ImitationServerBase):
#
#     response = ServerResponse()
#
#
# class ImitationClient(ImitationClientBase):
#
#     request = ClientRequest()
#
#
# class Imitation:
#     clients = []
#     server = None
#
#     def __init__(self, cfg: Config):
#         self.init_server(
#             cfg.remote,
#             cfg.maximum_connections,
#         )
#         self.init_clients(
#             cfg.address,
#             cfg.maximum_connections,
#             cfg.imitation_delay,
#         )
#
#     def init_server(self, remote, number_of_clients):
#         self.server = ImitationServer(remote, number_of_clients)
#
#     def init_clients(self, address, number_of_clients, delay):
#         for _ in range(number_of_clients):
#             imitation_client = ImitationClient(address, delay)
#             self.clients.append(imitation_client)
#
#     def start(self):
#         self.server.start()
#         for imitation_client in self.clients:
#             imitation_client.start()
