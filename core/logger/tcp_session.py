import database.logger as db
from common.crud import CrudBase


class TcpSessionCrud(CrudBase):

    model = db.TcpSession
