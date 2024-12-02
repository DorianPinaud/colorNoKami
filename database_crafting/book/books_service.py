from database_crafting.log.interface import LogRepository
from database_crafting.book.interfaces import BookRepository
from database_crafting.api_data_fetcher.interfaces import (
    ApiDataFetcherFactory,
    ApiDataFetcher,
)


class BooksService:

    def __init__(
        self,
        log_repo: LogRepository,
        fetcher_factory: ApiDataFetcherFactory,
    ):
        self._log_repo = log_repo
        self._fetcher_factory = fetcher_factory

    def init(self):
        book_fetcher = self._fetcher_factory.create("book")
        book_fetcher.fetch()
        self._log_repo.derived_book_from_logs()
