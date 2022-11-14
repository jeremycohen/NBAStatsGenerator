import argparse
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Team, Game


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
# Users are required to either enter a team name or team city to query record info
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--team_nickname')
group.add_argument('--team_city')

parser.add_argument('--from_date', required=True, type=valid_date)
parser.add_argument('--to_date', required=True, type=valid_date)
args = parser.parse_args()

engine = create_engine('postgresql://localhost/postgres')
session = Session(engine, future=True)

# Calculate an aggregated list of wins and losses based on the queried team
wins = 0
losses = 0

# Gather all the home games and wins / losses
home_games = session.query(Game).join(Game.home_team).filter(
    Team.city == args.team_city if args.team_city else Team.name == args.team_nickname
).filter(
    Game.postseason.is_(False)
).filter(
    Game.date >= args.from_date
).filter(
    Game.date <= args.to_date
).all()
wins += len([g for g in home_games if g.home_team_score > g.away_team_score])
losses += len([g for g in home_games if g.away_team_score > g.home_team_score])

# Gather all the away games and wins / losses
away_games = session.query(Game).join(Game.away_team).filter(
    Team.city == args.team_city if args.team_city else Team.name == args.team_nickname
).filter(
    Game.postseason.is_(False)
).filter(
    Game.date >= args.from_date
).filter(
    Game.date <= args.to_date
).all()
losses += len([g for g in away_games if g.home_team_score > g.away_team_score])
wins += len([g for g in away_games if g.away_team_score > g.home_team_score])

# Aggregate all the games together, display the joint record, and list of results in that time span
games = sorted(home_games + away_games, key=lambda game: game.date)
print(f'Record: {wins}-{losses}')
for g in games:
    print(
        f'{g.away_team.city} {g.away_team.name} {g.away_team_score} - '
        f'{g.home_team.city} {g.home_team.name} {g.home_team_score} ({g.date})'
    )
