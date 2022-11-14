import sys
import time
import unittest
from unittest import mock

from api.rate_limiter import RateLimiter


class RateLimiterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.currentTimestamp = time.time()

    def testMultipleRequestsDroppingPerRequest(self):
        rate_limiter = RateLimiter(max_requests=3, timeout=60)
        self.assertEqual(3, rate_limiter.num_requests_can_execute())
        rate_limiter.increment_request_count(1)
        self.assertEqual(2, rate_limiter.num_requests_can_execute())
        rate_limiter.increment_request_count(1)
        self.assertEqual(1, rate_limiter.num_requests_can_execute())
        rate_limiter.increment_request_count(1)
        self.assertEqual(0, rate_limiter.num_requests_can_execute())

    def testAddingMultipleRequests(self):
        rate_limiter = RateLimiter(max_requests=3, timeout=60)
        self.assertEqual(3, rate_limiter.num_requests_can_execute())
        rate_limiter.increment_request_count(3)
        self.assertEqual(0, rate_limiter.num_requests_can_execute())

    @unittest.mock.patch('time.time')
    def testResettingRateLimitWithTimeExpiry(self, time_mock):
        self.resetRateLimit = False

        def time_method():
            if self.resetRateLimit:
                return sys.float_info.max
            return 0

        time_mock.side_effect = time_method
        rate_limiter = RateLimiter(max_requests=3, timeout=0)
        self.assertEqual(3, rate_limiter.num_requests_can_execute())
        rate_limiter.increment_request_count(num_requests=3, cur_time=1)
        self.assertEqual(0, rate_limiter.num_requests_can_execute())
        self.resetRateLimit = True
        self.assertEqual(3, rate_limiter.num_requests_can_execute())
