from sqlalchemy import Column, Integer, ForeignKey

from models.base import DefaultBase


class Stat(DefaultBase):
    """
    Represents an NBA basketball stat for a given game and player
    """
    __tablename__ = 'stat'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    player_id = Column(Integer, ForeignKey('player.id'))
    team_id = Column(Integer, ForeignKey('team.id'))
    points = Column(Integer)
    assists = Column(Integer)
    rebounds = Column(Integer)
    blocks = Column(Integer)
    steals = Column(Integer)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fta = Column(Integer)
    ftm = Column(Integer)
