from api.base import BaseApi


class PlayersApi(BaseApi):

    @property
    def api_path(self) -> str:
        return 'players'
