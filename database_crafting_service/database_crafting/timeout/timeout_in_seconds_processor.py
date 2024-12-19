from database_crafting.timeout.interface import (
    TimeoutProcessor,
    TimeoutProcessorFactory,
)

import time


class TimeoutInSecondProcessor(TimeoutProcessor):

    def __init__(self, timeout_time_in_seconds: int):
        self._start_time = time.time()
        self._timeout_time_in_seconds = timeout_time_in_seconds

    def has_timeout(self) -> bool:
        return (time.time() - self._start_time) > self._timeout_time_in_seconds * 1000


class TimeoutInSecondProcessorFactory(TimeoutProcessorFactory):

    def __init__(self, timeout_time_in_seconds: int):
        self._timeout_time_in_seconds = timeout_time_in_seconds

    def create(self):
        return TimeoutInSecondProcessor(self._timeout_time_in_seconds)
