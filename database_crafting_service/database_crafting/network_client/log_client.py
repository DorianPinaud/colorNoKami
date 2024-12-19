from __future__ import annotations

from database_crafting.network_client.interface import NetworkClient
from database_crafting.log.interface import LogRepository
import time
import httpx


class LogClient(NetworkClient):
    _cache: LogRepository
    _number_request: int
    _request_per_minute: int
    _timestamp: float

    def __init__(self, cache, request_per_minute: int = 30):
        self._cache = cache
        self._number_request = 0
        self._request_per_minute = request_per_minute
        self._timestamp = time.time()

    def get(self, url: str, rate: float = 60.0):
        if not self._cache.is_logged(url):
            self._number_request += 1
            if self._number_request > self._request_per_minute:
                sleep_duration = max(70.0 - (time.time() - self._timestamp), 0.0)
                time.sleep(sleep_duration)
                self._number_request = 1
                self._timestamp = time.time()
            time.sleep(0.5)
            response = httpx.get(url)
            if response.status_code == 404:
                raise Exception(
                    f"Failed to contact api [{response.status_code}] {response.text},"
                )
            data_json = response.json()
            self._cache.register_log(url, data_json)
            return data_json
        else:
            return self._cache.get_log(url)
