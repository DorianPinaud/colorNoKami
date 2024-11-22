from abc import ABC, abstractmethod


class ApiData(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class ApiDataFactory(ABC):

    @abstractmethod
    def create_api_data(self, type: str) -> ApiData:
        pass
