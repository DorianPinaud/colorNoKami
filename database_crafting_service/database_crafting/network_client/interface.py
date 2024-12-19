from abc import ABC, abstractmethod


class NetworkClient(ABC):

    @abstractmethod
    def get(self, url: str, rate: float = 60):
        pass
