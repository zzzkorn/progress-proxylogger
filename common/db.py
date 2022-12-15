import logging
from datetime import datetime
from enum import Enum as EnumType
from pprint import pprint
from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# flake8: noqa: E402
import log


class MessageType(EnumType):
    packet = "пакет данных"
    info = "отладочная информация"
    error = "ошибка"


class PacketType(EnumType):
    received = "принятый пакет"
    sent = "отправленный пакет"


Base = declarative_base()


class Device(Base):
    __tablename__ = "logger_device"
    __title__ = "Устройство"

    id = Column(Integer, primary_key=True)

    description = Column(
        String(200),
        nullable=True,
        comment="Описание",
    )

    ip_address = Column(
        String(30),
        comment="Адресс",
        nullable=False,
        unique=True,
    )

    def __str__(self):
        if self.description:
            return f"{self.ip_address} {self.description}"
        return f"{self.ip_address}"

    def __repr__(self):
        if self.description:
            return f"{self.ip_address} {self.description}"
        return f"{self.ip_address}"


class Message(Base):
    __tablename__ = "logger_message"
    __title__ = "Сообщение"

    id = Column(Integer, primary_key=True)

    timestamp = Column(
        DateTime,
        default=datetime.now(),
    )

    message_type = Column(
        Enum(MessageType, name="message_type"),
        nullable=False,
        comment="Тип документа",
    )

    packet_type = Column(
        Enum(PacketType, name="packet_type"),
        comment="Тип пакета",
    )

    raw_data = Column(
        LargeBinary,
        comment="Сырые данные",
    )

    data = Column(
        String,
        comment="Данные",
    )

    device_id = Column(
        Integer,
        ForeignKey(Device.id),
        nullable=False,
        comment="К какому устройству относится",
    )

    device = relationship(
        Device,
        foreign_keys=[device_id],
    )

    def __str__(self):
        return (
            f"{self.timestamp} . {self.device}. "
            f"Данные: {self.data or self.raw_data}"
        )

    def __repr__(self):
        return (
            f"{self.timestamp} . {self.device}. "
            f"Данные: {self.data or self.raw_data}"
        )


class LoggerDatabase:

    logger = logging.getLogger("logger")

    def __init__(self, engine: str, file_log: bool = True):
        self.file_log = file_log
        self.engine = create_engine(
            engine,
            echo=False,
            pool_recycle=7200,
        )
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def _insert_device(self, ip_address, description=None):
        device = Device(ip_address=ip_address, description=description)
        self.session.add(device)
        self.session.commit()
        if self.file_log:
            self.logger.info(f"Добавлено устройство {device}")
        return device

    def _find_device(self, ip_address) -> Device:
        device = (
            self.session.query(Device)
            .filter_by(
                ip_address=ip_address,
            )
            .first()
        )
        if not device:
            device = self._insert_device(ip_address=ip_address)
        return device

    def _insert_packet(
        self,
        device_ip: str,
        raw_data: bytes,
        packet_type: PacketType,
    ):
        device = self._find_device(device_ip)
        packet = Message(
            device=device,
            raw_data=raw_data,
            message_type=MessageType.packet,
            packet_type=packet_type,
            timestamp=datetime.now(),
        )
        if self.file_log:
            self.logger.info(
                f"{MessageType.packet}-{packet_type}. {device}: {raw_data}"
            )
        self.session.add(packet)
        self.session.commit()

    def insert_sent_packet(self, device_ip: str, raw_data: bytes):
        self._insert_packet(device_ip, raw_data, PacketType.sent)

    def insert_received_packet(self, device_ip: str, raw_data: bytes):
        self._insert_packet(device_ip, raw_data, PacketType.received)

    def insert_info(self, device_ip: str, data: str):
        device = self._find_device(device_ip)
        info = Message(
            device=device,
            data=data,
            message_type=MessageType.info,
        )
        if self.file_log:
            self.logger.info(f"{MessageType.info}. {device}: {data}")
        self.session.add(info)
        self.session.commit()

    def insert_error(self, device_ip: str, data: str):
        device = self._find_device(device_ip)
        error = Message(
            device=device,
            data=data,
            message_type=MessageType.error,
        )
        if self.file_log:
            self.logger.error(f"{MessageType.info}. {device}: {data}")
        self.session.add(error)
        self.session.commit()

    def message_history(self) -> List[Message]:
        return self.session.query(Message).order_by(Message.timestamp).all()

    def clear_history(self):
        self.session.query(Message).delete()
        self.session.commit()


if __name__ == "__main__":
    engine = "sqlite:///../test_base.db3"
    device_address = "192.196.0.1"
    test_db = LoggerDatabase(engine)
    test_db.clear_history()
    test_db.insert_info(device_address, "Установленно соединение")
    test_db.insert_sent_packet(device_address, b"Sent packet")
    test_db.insert_received_packet(device_address, b"Received packet")
    test_db.insert_error(device_address, "Произошла ошибке")
    test_db.insert_info(device_address, "Соединение прервано")
    pprint(test_db.message_history())
