from sqlalchemy import String, Column, Integer

from models.base import DefaultBase


class Team(DefaultBase):
    """
    Represents an NBA basketball team
    """
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    abbreviation = Column(String(3))
    city = Column(String(20))
    conference = Column(String(4))
    division = Column(String(15))
    name = Column(String(15))
