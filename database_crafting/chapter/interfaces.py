from abc import ABC, abstractmethod

from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory
from database_crafting.book.interfaces import BookRepository
from database_crafting.domain.chapter import (
    Chapter,
    ChapterPair,
    ChapterPairWithScansUrls,
)

from typing import List


class ChapterRepository(ABC):

    @abstractmethod
    def get_chapters(self) -> List[Chapter]:
        pass

    @abstractmethod
    def get_chapters_count(self) -> int:
        pass


class ChapterPairRepository(ABC):

    @abstractmethod
    def get_chapters_pair(self) -> List[ChapterPair]:
        pass

    @abstractmethod
    def get_chapters_pair_count(self) -> int:
        pass


class EnrichChaptersPairwithScansUrlsService(ABC):

    @abstractmethod
    def enrich(self) -> None:
        pass


class ChapterPairWithScansUrlsRepository(ABC):

    @abstractmethod
    def get_chapter_pair_with_scans_urls(self) -> List[ChapterPairWithScansUrls]:
        pass

    @abstractmethod
    def get_chapters_pair_with_scans_urls_count(self) -> int:
        pass
