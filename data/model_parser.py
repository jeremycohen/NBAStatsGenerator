import datetime

from models import *


# TODO clean up model parsing to make it easier to remap field names

def parse_games(games: list[dict[str, any]]) -> list[Game]:
    """
    :param games: A list of dict-formatted untyped Game types
    :return: The SQLAlchemy-based typed Game models with properly converted type names
    """
    cols = [c.key for c in Game.__table__.columns]
    cols.remove('home_team_id')
    cols.remove('away_team_id')
    cols.remove('away_team_score')
    cols.remove('date')
    models = [Game(**{
        k: v for k, v in g.items() if k in cols
    }) for g in games]
    for untyped, typed in zip(games, models):
        typed.away_team_id = untyped['visitor_team']['id']
        typed.home_team_id = untyped['home_team']['id']
        typed.date = datetime.datetime.fromisoformat(untyped['date']).date()
        typed.away_team_score = untyped['visitor_team_score']
    return models


def parse_teams(teams: list[dict[str, any]]) -> list[Team]:
    """
    :param teams: A list of dict-formatted untyped Team types
    :return: The SQLAlchemy-based typed Team models with properly converted type names
    """
    cols = [c.key for c in Team.__table__.columns]
    return [Team(**{
        k: v for k, v in t.items() if k in cols
    }) for t in teams]


def parse_players(players: list[dict[str, any]]) -> list[Player]:
    """
    :param players: A list of dict-formatted untyped Player types
    :return: The SQLAlchemy-based typed Player models with properly converted type names
    """
    cols = [c.key for c in Player.__table__.columns]
    cols.remove('current_team_id')
    models = [Player(**{
        k: v for k, v in g.items() if k in cols
    }) for g in players]
    for untyped, typed in zip(players, models):
        typed.current_team_id = untyped['team']['id']
    return models


def parse_stats(stats: list[dict[str, any]]) -> list[Stat]:
    """
    :param stats: A list of dict-formatted untyped Stat types
    :return: The SQLAlchemy-based typed Stat models with properly converted type names
    """
    stats = [s for s in stats if s['player'] is not None]
    renamed_cols = {'assists', 'rebounds', 'blocks', 'steals', 'points', 'player_id', 'game_id', 'team_id'}
    cols = [c.key for c in Stat.__table__.columns if c.key not in renamed_cols]
    models = [Stat(**{
        k: v for k, v in s.items() if k in cols
    }) for s in stats]
    for untyped, typed in zip(stats, models):
        typed.assists = untyped['ast']
        typed.blocks = untyped['blk']
        typed.steals = untyped['stl']
        typed.points = untyped['pts']
        typed.game_id = untyped['game']['id']
        typed.player_id = untyped['player']['id']
        typed.team_id = untyped['team']['id']
    return models
