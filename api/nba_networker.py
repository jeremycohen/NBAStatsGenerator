import os

import aiohttp

DOMAIN = 'https://free-nba.p.rapidapi.com'


class NbaApiNetworker:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": os.environ['RAPIDAPI_KEY'],
            "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
        }

    async def get_total_pages(self,
                              api_path: str,
                              season: int,
                              per_page: int = 100) -> int:
        return (await self.__get_response(api_path=api_path,
                                          season=season,
                                          page_id=1,
                                          per_page=per_page))['meta']['total_pages']

    async def get_data(self,
                       api_path: str,
                       season: int,
                       page_id: int = 1,
                       per_page: int = 100):
        return (await self.__get_response(api_path=api_path,
                                          season=season,
                                          page_id=page_id,
                                          per_page=per_page))['data']

    async def __get_response(
        self,
        api_path: str,
        season: int,
        page_id: int = 1,
        per_page: int = 100
    ) -> dict:
        # TODO: use a URL generation library here
        url = f"{DOMAIN}/{api_path}"
        querystring = {"page": f"{page_id}", "per_page": f"{per_page}", "seasons[]": f"{season}"}

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=querystring) as resp:
                resp.raise_for_status()
                return await resp.json()
