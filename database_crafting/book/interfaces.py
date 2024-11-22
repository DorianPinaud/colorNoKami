from abc import ABC, abstractmethod
from database_crafting.domain.book import Book
from database_crafting.api_data.interfaces import ApiDataFactory
from typing import List


class BookRepository(ABC):

    @abstractmethod
    def fetch_books(self, api_data_factory: ApiDataFactory) -> None:
        pass

    @abstractmethod
    def get_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_books_count(self) -> int:
        pass
