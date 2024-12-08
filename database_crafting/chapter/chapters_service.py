from database_crafting.book.interfaces import BookRepository
from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory
from database_crafting.book.interfaces import PairChaptersBybookService
from database_crafting.chapter.interfaces import (
    ChapterPairRepository,
    EnrichChaptersPairwithScansUrlsService,
)
from database_crafting.log.interface import LogDerivedDataProcessor
import time
from database_crafting.timeout.timeout_in_seconds_processor import (
    TimeoutInSecondProcessorFactory,
)
from database_crafting.timeout.timeout_iterator import TimeoutIterator


class ChaptersService:

    def __init__(
        self,
        book_repo: BookRepository,
        fetch_factory: ApiDataFetcherFactory,
        derived_chapters: LogDerivedDataProcessor,
        derived_scansurls: LogDerivedDataProcessor,
        chapter_pair_repo: ChapterPairRepository,
        pairing_service: PairChaptersBybookService,
        enrichment_service: EnrichChaptersPairwithScansUrlsService,
    ):
        self._book_repo = book_repo
        self._fetch_factory = fetch_factory
        self._derived_chapters = derived_chapters
        self._derived_scansurls = derived_scansurls
        self._chapter_pair_repo = chapter_pair_repo
        self._pairing_service = pairing_service
        self._enrichment_service = enrichment_service

    def init(self, fetch_max_time_in_sec=None):

        start_time = time.time()

        for book in TimeoutIterator(
            self._book_repo.get_books(), TimeoutInSecondProcessorFactory(1)
        ):
            self._fetch_factory.create(
                "chapter_feed", params=[book.monochrome_id]
            ).fetch()
            self._fetch_factory.create(
                "chapter_feed", params=[book.fullcolor_id]
            ).fetch()

        self._derived_chapters.derived()
        self._pairing_service.pairing()

        for chapter in self._chapter_pair_repo.get_chapters_pair():
            self._fetch_factory.create(
                "chapter_url", params=[chapter.monochrome_chapter.id]
            ).fetch()
            self._fetch_factory.create(
                "chapter_url", params=[chapter.chromatic_chapter.id]
            )
            if (
                fetch_max_time_in_sec
                and (time.time() - start_time) > fetch_max_time_in_sec
            ):
                break

        self._derived_scansurls.derived()
        self._enrichment_service.enrich()
