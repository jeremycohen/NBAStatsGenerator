from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData(schema='nba')
