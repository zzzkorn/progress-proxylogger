from sqlalchemy.orm import Session


class SessionMixin:
    session: Session

    def init_session(self, engine):
        self.session = Session(engine)

    def commit(self):
        self.session.commit()
        self.session.close()
