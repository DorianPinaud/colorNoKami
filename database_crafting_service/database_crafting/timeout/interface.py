from abc import ABC, abstractmethod


class TimeoutProcessor(ABC):

    @abstractmethod
    def has_timeout(self) -> bool:
        pass


class TimeoutProcessorFactory(ABC):

    @abstractmethod
    def create(self) -> TimeoutProcessor:
        pass
