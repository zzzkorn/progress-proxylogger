from core.logger.message import ErrorCrud
from core.logger.message import InfoCrud
from core.logger.message import MessageCrud
from core.logger.message import PacketCrud
from core.logger.tcp_session import TcpSessionCrud


class LoggerCore:
    def __init__(self):
        self.message = MessageCrud()
        self.packets = PacketCrud()
        self.info = InfoCrud()
        self.errors = ErrorCrud()
        self.tcp_sessions = TcpSessionCrud()
