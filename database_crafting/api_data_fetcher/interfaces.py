from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class ApiDataFetcher(ABC):

    @abstractmethod
    def fetch(self):
        pass


class ApiDataFetcherFactory(ABC):

    @abstractmethod
    def create(self, type_name: str, params: List[str] = []) -> ApiDataFetcher:
        pass
