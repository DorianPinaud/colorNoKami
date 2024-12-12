from database_crafting.interfaces import DatabaseCraftingPipeline, DatabaseCraftingStage

from database_crafting.log.interface import LogDerivedDataProcessor
from database_crafting.book.interfaces import BookRepository, PairChaptersBybookService
from database_crafting.api_data_fetcher.interfaces import (
    ApiDataFetcherFactory,
    ApiDataFetcher,
)
from database_crafting.timeout.interface import TimeoutProcessorFactory
from database_crafting.timeout.timeout_iterator import TimeoutIterator
from database_crafting.chapter.interfaces import (
    EnrichChaptersPairwithScansUrlsService,
    ChapterPairRepository,
)

from typing import List


class ChapterPairCraftingStage(DatabaseCraftingStage):

    def __init__(
        self,
        pairing_service: PairChaptersBybookService,
        chapter_pair_repo: ChapterPairRepository,
        enrichment_service: EnrichChaptersPairwithScansUrlsService,
        fetcher_factory: ApiDataFetcherFactory,
        derived_data: LogDerivedDataProcessor,
        timeout_processor_factory: TimeoutProcessorFactory,
    ):
        self._pairing_service = pairing_service
        self._chapter_pair_repo = chapter_pair_repo
        self._derived_data = derived_data
        self._enrichment_service = enrichment_service
        self._fetcher_factory = fetcher_factory
        self._timeout_processor_factory = timeout_processor_factory

    def execute(self):
        self._pairing_service.pairing()
        for chapter in TimeoutIterator(
            self._chapter_pair_repo.get_chapters_pair(), self._timeout_processor_factory
        ):
            self._fetcher_factory.create(
                "chapter_url", params=[chapter.monochrome_chapter.id]
            ).fetch()
            self._fetcher_factory.create(
                "chapter_url", params=[chapter.chromatic_chapter.id]
            )

        self._derived_data.derived()
        self._enrichment_service.enrich()


class ChapterCraftingStage(DatabaseCraftingStage):

    def __init__(
        self,
        book_repo: BookRepository,
        fetcher_factory: ApiDataFetcherFactory,
        derived_data: LogDerivedDataProcessor,
        timeout_processor_factory: TimeoutProcessorFactory,
    ):
        self._book_repo = book_repo
        self._fetcher_factory = fetcher_factory
        self._derived_data = derived_data
        self._timeout_processor_factory = timeout_processor_factory

    def execute(self):
        for book in TimeoutIterator(
            self._book_repo.get_books(), self._timeout_processor_factory
        ):
            self._fetcher_factory.create(
                "chapter_feed", params=[book.monochrome_id]
            ).fetch()
            self._fetcher_factory.create(
                "chapter_feed", params=[book.fullcolor_id]
            ).fetch()

        self._derived_data.derived()


class BookCraftingStage(DatabaseCraftingStage):

    def __init__(
        self,
        derived_data: LogDerivedDataProcessor,
        fetcher_factory: ApiDataFetcherFactory,
    ):
        self.derived_data = derived_data
        self._fetcher_factory = fetcher_factory

    def execute(self):
        book_fetcher = self._fetcher_factory.create("book")
        book_fetcher.fetch()
        self.derived_data.derived()
