# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import logging
import sys

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.games import GamesApi
from api.nba_networker import NbaApiNetworker
from api.players import PlayersApi
from api.rate_limiter import RateLimiter
from api.teams import TeamsApi
from data.dao import Dao
from data.model_parser import parse_teams, parse_games, parse_players
from models.base import DefaultBase


async def run():
    """"
    The parsing logic operates as follows:
    - Runs all the API requests using a shared rate limiter (to make sure all requests respect the global API limits)
    - Clears prior table contents
    - Writes the team info to the tables (as those have no data dependencies)
    - Writes the player and game info to the tables (as those have relations with the team objects)
    """
    rate_limiter = RateLimiter(max_requests=60, timeout=60)
    networker = NbaApiNetworker()
    logging.info('Fetching team info')
    teams = parse_teams(await (TeamsApi(rate_limiter=rate_limiter, networker=networker, timeout_time=60)).get_data())
    logging.info('Fetching game info')
    games = parse_games(await (GamesApi(rate_limiter=rate_limiter, networker=networker, timeout_time=60)).get_data())
    logging.info('Fetching players info')
    players = parse_players(await (PlayersApi(rate_limiter=rate_limiter, networker=networker, timeout_time=60)).get_data())
    # TODO figure out why at the API level some games in the stats table aren't in the games table
    # stats = parse_stats(await (StatsApi(rate_limiter=rate_limiter, networker=networker, timeout_time=5)).get_data())

    engine = create_async_engine('postgresql+asyncpg://localhost/postgres')
    async with engine.begin() as conn:
        await conn.run_sync(DefaultBase.metadata.drop_all)
        await conn.run_sync(DefaultBase.metadata.create_all)

    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()

    async with Dao(session) as dao:
        dao.save_teams(teams)

    async with Dao(session) as dao:
        dao.save_games(games)
        dao.save_players(players)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # TODO: refactor and move logging initialization to its own file
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s:%(lineno)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    asyncio.run(run())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
