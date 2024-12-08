from database_crafting.timeout.interface import TimeoutProcessorFactory
from typing import Iterable, TypeVar, Generator, Generic

T = TypeVar("T")


class TimeoutIterator(Generic[T]):

    def __init__(
        self, iterable: Iterable[T], timeout_processor_factory: TimeoutProcessorFactory
    ):
        self._iterable = iterable
        self._timeout_processor_factory = timeout_processor_factory

    def __iter__(self) -> Generator[T, None, None]:
        timeout_processor = self._timeout_processor_factory.create()
        for item in self._iterable:
            if timeout_processor.has_timeout():
                return
            yield item
