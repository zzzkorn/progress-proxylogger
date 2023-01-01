from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property

from database.logger.common import Base


class TcpSession(Base):
    __title__ = "Сеанс TCP соединения"

    id = Column(Integer, primary_key=True)
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=False)

    def __message_list(self):
        return "\n".join(str(message) for message in self.messages)

    @hybrid_property
    def processed(self):
        for message in self.messages:
            if not message.processed:
                return False
        return True

    def __str__(self):
        return f"{self.id}. {self.host}:{self.port}:\n {self.messages}"

    def __repr__(self):
        return f"{self.id}. {self.host}:{self.port}:\n {self.messages}"
