from database_crafting.interfaces import DatabaseCraftingPipeline, DatabaseCraftingStage

from database_crafting.database_crafting_stages import (
    BookCraftingStage,
    ChapterCraftingStage,
    ChapterPairCraftingStage,
)

from pymongo.database import Database

from typing import List

from database_crafting.network_client.log_client import LogClient
from database_crafting.log.mongo_log_repository import MongoLogRepository
from database_crafting.book.mongo_book_repository import MongoBookRepository
from database_crafting.chapter.mongo_chapter_pair_repository import (
    MongoChapterPairRepository,
)
from database_crafting.log.mongo_log_derived_processors import (
    MongoLogDerivedBooks,
    MongoLogDerivedChapters,
    MongoLogDerivedScansUrls,
)
from database_crafting.api_data_fetcher.manga_dex_api_data_fetcher_factory import (
    MangaDexApiDataFetcherFactory,
)
from database_crafting.timeout.interface import (
    TimeoutProcessorFactory,
)
from database_crafting.book.mongo_pair_chapters_by_book_service import (
    MongoChaptersByBookPairer,
)
from database_crafting.chapter.mongo_enrich_chapters_pair_with_scansurls_service import (
    MongoChaptersPairwithScansUrlsEnricher,
)


class MongoDatabaseCraftingPipeline(DatabaseCraftingPipeline):

    def __init__(
        self,
        db: Database,
        timeout_processor_factory: TimeoutProcessorFactory,
    ):
        log_repo = MongoLogRepository(db)
        log_client = LogClient(log_repo)
        api_data_fetcher_factory = MangaDexApiDataFetcherFactory(log_client)
        book_repo = MongoBookRepository(db)
        log_derived_book = MongoLogDerivedBooks(db)
        log_derived_chapter = MongoLogDerivedChapters(db)
        log_derived_scansurls = MongoLogDerivedScansUrls(db)
        pair_chapter_service = MongoChaptersByBookPairer(db)
        enrich_chapterpair = MongoChaptersPairwithScansUrlsEnricher(db)
        chapterpair_repo = MongoChapterPairRepository(db)

        self._stages = [
            BookCraftingStage(log_derived_book, api_data_fetcher_factory),
            ChapterCraftingStage(
                book_repo,
                api_data_fetcher_factory,
                log_derived_chapter,
                timeout_processor_factory,
            ),
            ChapterPairCraftingStage(
                pair_chapter_service,
                chapterpair_repo,
                enrich_chapterpair,
                api_data_fetcher_factory,
                log_derived_scansurls,
                timeout_processor_factory,
            ),
        ]

    def get_stages(self) -> List[DatabaseCraftingStage]:
        return self._stages

    def execute(self):
        for stage in self._stages:
            stage.execute()
