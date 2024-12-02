from abc import ABC, abstractmethod

from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory
from database_crafting.book.interfaces import BookRepository
from database_crafting.domain.chapter import Chapter, ChapterPaired

from typing import List


class ChapterRepository(ABC):

    @abstractmethod
    def get_chapters(self) -> List[Chapter]:
        pass

    @abstractmethod
    def get_chapters_count(self) -> int:
        pass

    @abstractmethod
    def get_chapters_paired(self) -> List[ChapterPaired]:
        pass

    @abstractmethod
    def get_chapters_paired_count(self) -> int:
        pass
