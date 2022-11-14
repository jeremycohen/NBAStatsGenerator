from api.base import BaseApi


class TeamsApi(BaseApi):

    @property
    def api_path(self) -> str:
        return 'teams'
