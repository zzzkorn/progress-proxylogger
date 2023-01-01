from core.loger.message import ErrorCrud
from core.loger.message import InfoCrud
from core.loger.message import MessageCrud
from core.loger.message import PacketCrud
from core.loger.tcp_session import TcpSessionCrud


class LoggerCore:
    def __init__(self):
        self.message = MessageCrud()
        self.packets = PacketCrud()
        self.info = InfoCrud()
        self.errors = ErrorCrud()
        self.tcp_sessions = TcpSessionCrud()


class ParseCore:
    def __init__(self):
        pass
