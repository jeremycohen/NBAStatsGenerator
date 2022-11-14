import unittest
from unittest import mock
from unittest.mock import MagicMock, AsyncMock

from api.base import BaseApi


class TestSubclassApi(BaseApi):
    def api_path(self) -> str:
        return 'foo'


class BaseApiTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # Setup instances of rate limiter mock and networker mock that can be utilized in tests to stub responses
        self.rate_limiter_mock = MagicMock()
        self.networker_mock = MagicMock()
        self.base_api = TestSubclassApi(networker=self.networker_mock,
                                        rate_limiter=self.rate_limiter_mock,
                                        timeout_time=0)

    async def testGetMultipleValues(self):
        self.increment = 1

        def get_data(*args, **kwargs):
            r = [self.increment]
            self.increment += 1
            return r

        self.networker_mock.get_data = AsyncMock(side_effect=get_data)
        self.networker_mock.get_total_pages = AsyncMock(return_value=4)
        self.rate_limiter_mock.num_requests_can_execute = MagicMock(return_value=4)
        data = await self.base_api.get_data()
        self.assertEqual(data, [1, 2, 3, 4])

    async def testRateLimiterChecked(self):
        self.networker_mock.get_data = AsyncMock(return_value=[{'a': 'b'}])
        self.networker_mock.get_total_pages = AsyncMock(return_value=3)
        self.rate_limiter_mock.num_requests_can_execute = MagicMock(return_value=4)  # Add an extra request for metadata
        data = await self.base_api.get_data()
        self.assertEqual(data, [{'a': 'b'}, {'a': 'b'}, {'a': 'b'}])

    async def testWaitCalledWhenRateLimited(self):
        self.networker_mock.get_data = AsyncMock(return_value=[{'a': 'b'}])
        self.networker_mock.get_total_pages = AsyncMock(return_value=3)
        with mock.patch('asyncio.sleep', new_callable=AsyncMock) as sleep_mock:
            self.firstRateLimitCheck = True

            def can_execute(*args, **kwargs):
                if self.firstRateLimitCheck:
                    self.firstRateLimitCheck = False
                    return -1
                return 3

            self.rate_limiter_mock.num_requests_can_execute = MagicMock(side_effect=can_execute)
            await self.base_api.get_data()

            # Check that we successfully followed the rate limit
            sleep_mock.assert_called()

            data = await self.base_api.get_data()
            self.assertEqual(data, [{'a': 'b'}, {'a': 'b'}, {'a': 'b'}])

    async def testResultsAggregatedAcrossMultipleRequestIterations(self):
        self.networker_mock.get_data = AsyncMock(return_value=[{'a': 'b'}])
        self.networker_mock.get_total_pages = AsyncMock(return_value=3)
        self.rate_limiter_mock.num_requests_can_execute = MagicMock(return_value=1)
        data = await self.base_api.get_data()
        self.assertEqual(data, [{'a': 'b'}, {'a': 'b'}, {'a': 'b'}])
        # Additionally, check that we incremented the request count 3 times to indicate we did 3 sets of requests as we
        # can only issue 1 request at a time
        self.rate_limiter_mock.increment_request_count.assert_has_calls([mock.call(1), mock.call(1), mock.call(1)])

    async def testOnlyPullingTotalPagesSpecified(self):
        self.networker_mock.get_data = AsyncMock(return_value=[{'a': 'b'}])
        self.networker_mock.get_total_pages = AsyncMock(return_value=2)
        self.rate_limiter_mock.num_requests_can_execute = MagicMock(return_value=3)
        data = await self.base_api.get_data()
        self.assertEqual(data, [{'a': 'b'}, {'a': 'b'}])
