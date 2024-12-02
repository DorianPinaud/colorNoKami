from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory
from database_crafting.book.interfaces import BookRepository
from database_crafting.log.interface import LogRepository


class ChaptersService:

    def __init__(
        self,
        fetch_factory: ApiDataFetcherFactory,
        book_repo: BookRepository,
        log_repo: LogRepository,
    ):
        self._fetch_factory = fetch_factory
        self._book_repo = book_repo
        self._log_repo = log_repo

    def init(self):

        for book in self._book_repo.get_books():
            self._fetch_factory.create(
                "chapter_feed", params=[book.monochrome_id]
            ).fetch()
            self._fetch_factory.create(
                "chapter_feed", params=[book.fullcolor_id]
            ).fetch()
        self._log_repo.derived_chapters_from_logs()
        self._book_repo.pair_chapter_by_book()
