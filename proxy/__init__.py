import logging
import socket
import sys
import threading

# flake8: noqa: E402
import log
from common.conf import Config
from common.mixins import SessionMixin
from core.logger import LoggerCore
from database.logger import Error
from database.logger import Packet
from database.logger import PacketType
from database.logger import TcpSession
from database.logger.common import InitLoggerModelsMixin

logger = logging.getLogger("logger")


class Server(InitLoggerModelsMixin):

    logger = logger

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.sock = None
        self.init_database(cfg.database_engine)

    def init_socket(self):
        self.logger.info(
            f"Запущен сервер {self.cfg.address}. Если адрес не указан, "
            f"принимаются соединения с любых адресов."
        )
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.cfg.address)
        self.sock.listen(self.cfg.maximum_connections)

    def run(self):
        # Инициализация Сокета
        self.init_socket()

        # Основной цикл программы сервера
        while True:
            try:
                client, client_address = self.sock.accept()
                self.logger.info(
                    f"Установлено соедение {self.cfg.address} с "
                    f"{client_address}"
                )
                self.process_client_message(client)
            except KeyboardInterrupt:
                self.sock.close()
                logger.info(f"Соедение {self.cfg.address} прервано")
                sys.exit(1)

    def process_client_message(self, client):
        message = client.recv(self.cfg.max_package_length)
        proxy = Proxy(
            self.cfg,
            self.engine,
            client,
            message,
        )
        # proxy.daemon = True
        proxy.start()


class Proxy(SessionMixin, threading.Thread):

    core = LoggerCore()
    logger = logger
    tcp_session: TcpSession

    def _init_tcp_session(self):
        self.tcp_session = self.core.tcp_sessions.create(
            self.session,
            dict(
                host=self.device_address[0],
                port=self.device_address[1],
            ),
        )

    def _send_packet(self, packet):
        self.sock.send(packet)
        self.tcp_session.messages.append(
            Packet(
                raw=packet,
                packet_type=PacketType.sent,
            )
        )

    def _receive_packet(self):
        reply = self.sock.recv(self.cfg.max_package_length)
        if len(reply):
            self.tcp_session.messages.append(
                Packet(
                    raw=reply,
                    packet_type=PacketType.received,
                )
            )
            self.client.send(reply)
            return True
        else:
            return False

    def _error(self, e):
        self.tcp_session.messages.append(Error(data=f"{e}"))

    def __init__(
        self,
        cfg: Config,
        engine: object,
        client: socket,
        message: bytes,
    ):
        self.client = client
        self.sock = None
        self.message = message
        self.cfg = cfg
        self.device_address = client.getpeername()
        self.init_session(engine)
        super().__init__()

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.cfg.remote)
        self._init_tcp_session()

    def run(self):
        try:
            self.init_socket()
            self._send_packet(self.message)

            while True:
                if not self._receive_packet():
                    break

        except socket.error as e:
            self._error(e)
        finally:
            logger.info(f"{self.tcp_session}")
            self.sock.close()
            self.client.close()
            self.commit()
            sys.exit(1)
