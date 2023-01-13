import random

from common.generator import Generator
from common.generator import RelationFK
from database.logger import Error
from database.logger import Info
from database.logger import Packet
from database.logger import PacketType
from database.logger import TcpSession

generator = Generator()


def tcp_session_create_dict(session):
    return dict(
        host=".".join([f"{random.randint(0, 255)}" for _ in range(4)]),
        port=random.randint(10000, 60000),
    )


def packet_create_dict(session):
    return dict(
        session=RelationFK()(session, TcpSession),
        raw=b"Hello world!",
        packet_type=PacketType.sent,
    )


def info_message_create_dict(session):
    return dict(
        session=RelationFK()(session, TcpSession),
        data="Info message",
    )


def error_create_dict(session):
    return dict(
        session=RelationFK()(session, TcpSession),
        data="Info message",
    )


def create_tpc_session(session):
    values = tcp_session_create_dict(session)
    obj = TcpSession(**values)
    session.add(obj)
    session.flush()
    return obj.id


def create_packet(session):
    objects = []
    values = packet_create_dict(session)
    obj = Packet(**values)
    objects.append(obj)
    session.add(obj)
    values["packet_type"] = PacketType.received
    obj = Packet(**values)
    objects.append(obj)
    session.add(obj)
    session.flush()
    return [obj.id for obj in objects]


def create_info_message(session):
    values = info_message_create_dict(session)
    obj = Info(**values)
    session.add(obj)
    session.flush()
    return obj.id


def create_error(session):
    values = error_create_dict(session)
    obj = Error(**values)
    session.add(obj)
    session.flush()
    return obj.id


@generator.custom(count=10)
def tcp_sessions_for_read_page(session):
    return create_tpc_session(session)


@generator.custom(count=20)
def packets_for_read_page(session):
    return create_packet(session)


@generator.custom(count=20)
def info_messages_for_read_page(session):
    return create_info_message(session)


@generator.custom(count=20)
def errors_for_read_page(session):
    return create_error(session)
