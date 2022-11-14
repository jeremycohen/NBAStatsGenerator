from api.base import BaseApi


class GamesApi(BaseApi):

    @property
    def api_path(self) -> str:
        return 'games'
