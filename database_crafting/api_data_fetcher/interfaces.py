from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List, Iterable, Any

from database_crafting.domain.book import Book


class ApiDataFetcher(ABC):

    @abstractmethod
    def fetch(self):
        pass


class ApiDataFetcherFactory(ABC):

    @abstractmethod
    def create(self, type_name: str, params: List[str] = []) -> ApiDataFetcher:
        pass
