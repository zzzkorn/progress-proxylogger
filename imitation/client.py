import threading
import time
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

from common.variables import MAX_PACKAGE_LENGTH


class ImitationClientBase(threading.Thread):
    def __init__(self, address, delay):
        self.address = address
        self.delay = delay
        super().__init__()

    @property
    def request(self):
        raise NotImplementedError

    def run(self):
        while True:
            time.sleep(self.delay)
            sock = socket(AF_INET, SOCK_STREAM)
            try:
                sock.connect(self.address)
                sock.send(self.request())
                sock.recv(MAX_PACKAGE_LENGTH)
            finally:
                sock.close()
