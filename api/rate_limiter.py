import time
from typing import Optional


class RateLimiter:
    """
    Tracks requests that may be rate limited through making sure total number of requests, specified by `max_requests`,
    is not exceeded. This is done by keeping a map of number of requests made at a given time, and that entry is purged
    once the `timeout` has completed
    """
    def __init__(self, max_requests: int, timeout: int):
        self.max_requests = max_requests
        self.timeout = timeout
        # Map of request inputs to time
        self.request_input_map = {}

    def num_requests_can_execute(self) -> int:
        self.reset_state_if_timeouts_expired()
        return self.max_requests - self.get_total_requests()

    def increment_request_count(self, num_requests: int, cur_time: Optional[float] = None):
        if not cur_time:
            cur_time = time.time()
        if cur_time not in self.request_input_map:
            self.request_input_map[cur_time] = 0
        self.request_input_map[cur_time] += num_requests

    def get_total_requests(self):
        self.reset_state_if_timeouts_expired()
        return sum(self.request_input_map.values())

    def reset_state_if_timeouts_expired(self):
        self.request_input_map = {k: v for k, v in self.request_input_map.items() if
                                  k + self.timeout >= time.time()}
