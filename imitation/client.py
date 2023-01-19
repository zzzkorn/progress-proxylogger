import threading
import time
from copy import copy
from datetime import datetime
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket
from typing import Tuple
from typing import Union

from common.variables import MAX_PACKAGE_LENGTH
from imitation.variables import CLIENT_REGISTRATION_REQUEST_POSTFIX
from imitation.variables import CLIENT_REGISTRATION_REQUEST_PREFIX
from imitation.variables import CLIENT_REGISTRATION_RESPONSE
from imitation.variables import POINT_BASE
from imitation.variables import POINT_BASE_POSTFIX
from imitation.variables import POINTS


def get_points() -> bytes:
    for point in POINTS:
        timestamp = int(datetime.utcnow().timestamp()) - 0x4B3D3B00 + 3 * 3600
        timestamp = timestamp.to_bytes(4, byteorder="little", signed=True)
        yield POINT_BASE + timestamp + POINT_BASE_POSTFIX + point


def get_registration_request(imei_id: Union[str, int]) -> bytes:
    request = copy(CLIENT_REGISTRATION_REQUEST_PREFIX)
    if type(imei_id) == int:
        imei_id = str(imei_id)
    request += bytearray(imei_id, "utf-8")
    request += CLIENT_REGISTRATION_REQUEST_POSTFIX
    return request


class ImitationClient(threading.Thread):
    def __init__(
        self,
        address: Tuple,
        imei_id: Union[str, int],
        delay: int,
    ):
        self.address = address
        self.delay = delay
        self.sock = None
        self.registration_request = get_registration_request(imei_id)
        super().__init__()

    def registration(self):
        self.sock.send(self.registration_request)
        self.sock.recv(MAX_PACKAGE_LENGTH)
        self.sock.send(CLIENT_REGISTRATION_RESPONSE)

    def send_data(self):
        for point in get_points():
            time.sleep(self.delay)
            self.sock.send(point)
            self.sock.recv(MAX_PACKAGE_LENGTH)

    def run(self):
        while True:
            self.sock = socket(AF_INET, SOCK_STREAM)
            try:
                self.sock.connect(self.address)
                self.registration()
                self.send_data()
            finally:
                self.sock.close()


if __name__ == "__main__":
    imitation = ImitationClient(
        # ("127.0.0.1", 50101),
        ("213.219.245.116", 20100),
        # ("193.232.47.4", 40005),
        358887095658454,
        1,
    )
    imitation.start()
