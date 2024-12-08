from database_crafting.log.interface import LogDerivedDataProcessor
from database_crafting.book.interfaces import BookRepository
from database_crafting.api_data_fetcher.interfaces import (
    ApiDataFetcherFactory,
    ApiDataFetcher,
)


class BooksService:

    def __init__(
        self,
        derived_data: LogDerivedDataProcessor,
        fetcher_factory: ApiDataFetcherFactory,
    ):
        self.derived_data = derived_data
        self._fetcher_factory = fetcher_factory

    def init(self):
        book_fetcher = self._fetcher_factory.create("book")
        book_fetcher.fetch()
        self.derived_data.derived()
