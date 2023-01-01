from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from common.metaclasses import AutoTableNameMeta

metadata = MetaData()

Base = declarative_base(
    metadata=metadata,
    name="BaseModel",
    metaclass=AutoTableNameMeta,
)


class InitLoggerModelsMixin:

    engine: object

    def init_database(self, engine):
        self.engine = create_engine(
            engine,
            echo=False,
            pool_recycle=7200,
        )
        Base.metadata.create_all(self.engine)
