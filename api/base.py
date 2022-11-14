import asyncio
import itertools
import logging
from abc import ABC, abstractmethod

from api.nba_networker import NbaApiNetworker
from api.rate_limiter import RateLimiter


class BaseApi(ABC):
    """
    Base Api handling class that handles rate limiting, waiting for a specified timeout_time until the rate limit
    has been cleared, and issuing parallel network calls to a networker
    """
    def __init__(self, networker: NbaApiNetworker, rate_limiter: RateLimiter, timeout_time: float = 5.0):
        self.networker = networker
        self.rate_limiter = rate_limiter
        self.timeout_time = timeout_time

    @property
    @abstractmethod
    def api_path(self) -> str:
        ...

    @property
    def season(self) -> int:
        return 2021

    async def get_data(self):
        # Get the total before we iterate through the pages, so we know how many pages we need to fetch
        page_count = await self.networker.get_total_pages(season=self.season,
                                                          api_path=self.api_path)
        # Technically this hits the api with 1 request, so let the rate limiter know
        self.rate_limiter.increment_request_count(1)
        tasks = []
        logging.info(f'API {self.api_path}: fetching from {page_count} pages')

        # API starts at page 1, go through all the pages while respecting the rate limiter
        cur_page = 1
        while cur_page <= page_count:
            while self.rate_limiter.num_requests_can_execute() <= 0:
                logging.info(f'Hit rate limit, waiting for {self.timeout_time} seconds')
                await asyncio.sleep(self.timeout_time)
            pages_fetched = min(self.rate_limiter.num_requests_can_execute(), page_count - cur_page + 1)
            # Use a task group to issue multiple network requests through pages in parallel
            async with asyncio.TaskGroup() as tg:
                logging.info(f"Pulling {pages_fetched} pages for request {self.api_path}, starting at {cur_page}")
                for i in range(cur_page, cur_page + pages_fetched):
                    tasks.append(tg.create_task(self.networker.get_data(season=self.season,
                                                                        api_path=self.api_path,
                                                                        page_id=i)))
            self.rate_limiter.increment_request_count(pages_fetched)
            cur_page += pages_fetched
        return list(itertools.chain.from_iterable([t.result() for t in tasks]))
