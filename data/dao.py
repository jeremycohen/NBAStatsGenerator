from sqlalchemy.ext.asyncio import AsyncSession

from models import *


class Dao:
    """
    Provides a wrapper around sqlalchemy session handling to save different model objects
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.transaction = self.session.begin()
        await self.transaction.start()
        return self

    async def __aexit__(self, *args):
        await self.transaction.commit()
        await self.session.close()

    def save_teams(self, teams: list[Team]):
        self.session.add_all(teams)

    def save_games(self, games: list[Game]):
        self.session.add_all(games)

    def save_players(self, players: list[Player]):
        self.session.add_all(players)

    def save_stats(self, stats: list[Stat]):
        self.session.add_all(stats)
