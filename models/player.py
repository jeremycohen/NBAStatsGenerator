from sqlalchemy import String, Column, Integer, ForeignKey

from models.base import DefaultBase


class Player(DefaultBase):
    """
    Represents a basketball player data model
    """
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    current_team_id = Column(Integer, ForeignKey('team.id'))
    first_name = Column(String(30))
    last_name = Column(String(30))
    height_feet = Column(Integer)
    height_inches = Column(Integer)
    position = Column(String)
