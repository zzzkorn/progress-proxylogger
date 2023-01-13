import database.logger as db
from common import filter_fields
from common.crud import CrudBase


class MessageCrud(CrudBase):

    model = db.Message

    @property
    def filter_fields(self):
        return dict(
            processed=filter_fields.BooleanSelect(self.model.processed),
            session=filter_fields.Field(self.model.session),
        )


class PacketCrud(MessageCrud):
    model = db.Packet


class InfoCrud(MessageCrud):
    model = db.Info


class ErrorCrud(MessageCrud):
    model = db.Error
