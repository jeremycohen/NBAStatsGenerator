from api.base import BaseApi


class StatsApi(BaseApi):

    @property
    def api_path(self) -> str:
        return 'stats'
