import binascii
from enum import Enum as EnumType

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import relationship

from database.logger.common import Base


class MessageType(EnumType):
    packet = "пакет данных"
    info = "отладочная информация"
    error = "ошибка"


class PacketType(EnumType):
    received = "принятый пакет"
    sent = "отправленный пакет"


class Message(Base):
    __title__ = "Сообщение"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    type = Column(
        Enum(MessageType),
        nullable=False,
        comment="Тип сообщения",
    )

    timestamp = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    session_id = Column(
        Integer,
        ForeignKey("TcpSession.id"),
        nullable=False,
        comment="К какому сеансу связи относится",
    )

    session = relationship(
        "TcpSession",
        foreign_keys=[session_id],
        backref="messages",
    )

    processed = Column(
        Boolean,
        default=False,
        comment="Сообщение обработано",
    )

    __mapper_args__ = {
        "polymorphic_on": type,
    }


class Packet(Message):
    __title__ = "пакет данных"

    @declared_attr
    def id(self):
        return Column(
            Integer,
            ForeignKey(
                Message.id,
                ondelete="cascade",
            ),
            primary_key=True,
        )

    raw = Column(
        LargeBinary,
        comment="Сырые данные",
    )

    packet_type = Column(
        Enum(PacketType),
        nullable=False,
        comment="Тип пакета",
    )

    __mapper_args__ = {
        "polymorphic_identity": MessageType.packet,
    }

    def __str__(self):
        return f"ПАКЕТ. {self.packet_type}: {binascii.hexlify(self.raw)}"

    def __repr__(self):
        return f"ПАКЕТ. {self.packet_type}: {binascii.hexlify(self.raw)}"


class Info(Message):
    __title__ = "отладочная информация"

    @declared_attr
    def id(self):
        return Column(
            Integer,
            ForeignKey(
                Message.id,
                ondelete="cascade",
            ),
            primary_key=True,
        )

    data = Column(String, comment="Данные")

    __mapper_args__ = {
        "polymorphic_identity": MessageType.info,
    }

    def __str__(self):
        return f"ИНФО: {self.data}"

    def __repr__(self):
        return f"ИНФО: {self.data}"


class Error(Message):
    __title__ = "ошибка"

    @declared_attr
    def id(self):
        return Column(
            Integer,
            ForeignKey(
                Message.id,
                ondelete="cascade",
            ),
            primary_key=True,
        )

    data = Column(String, comment="Данные")

    __mapper_args__ = {
        "polymorphic_identity": MessageType.error,
    }

    def __str__(self):
        return f"ОШИБКА: {self.data}"

    def __repr__(self):
        return f"ОШИБКА: {self.data}"
