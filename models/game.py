from sqlalchemy import Boolean, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.base import DefaultBase


class Game(DefaultBase):
    """
    Represents a basketball game data model
    """
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey('team.id'))
    away_team_id = Column(Integer, ForeignKey('team.id'))
    home_team = relationship('Team', foreign_keys=[home_team_id])
    away_team = relationship('Team', foreign_keys=[away_team_id])
    home_team_score = Column(Integer)
    away_team_score = Column(Integer)
    postseason = Column(Boolean)
    date = Column(Date())
