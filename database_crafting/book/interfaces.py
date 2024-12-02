from abc import ABC, abstractmethod

from database_crafting.domain.book import Book
from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory


from typing import List


class BookRepository(ABC):

    @abstractmethod
    def get_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_books_count(self) -> int:
        pass

    @abstractmethod
    def pair_chapter_by_book(self) -> None:
        pass
