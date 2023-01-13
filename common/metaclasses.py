from sqlalchemy.orm import DeclarativeMeta


class AutoTableNameMeta(DeclarativeMeta):
    def __init__(self, name, bases, dict_):
        if "__tablename__" not in self.__dict__ and not self.__dict__.get(
            "__abstract__", False
        ):
            self.__tablename__ = name
        super(AutoTableNameMeta, self).__init__(name, bases, dict_)
