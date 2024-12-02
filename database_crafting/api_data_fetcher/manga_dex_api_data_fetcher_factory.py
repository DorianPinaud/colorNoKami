from database_crafting.api_data_fetcher.interfaces import (
    ApiDataFetcherFactory,
    ApiDataFetcher,
)
from database_crafting.api_data_fetcher.manga_dex_api_data_fetcher import (
    MangaDexApiDataFetcher,
)
from database_crafting.network_client.interface import NetworkClient
from abc import ABC, abstractmethod
from typing import Dict, List


class ApiDataCreationStartegy(ABC):

    @abstractmethod
    def create(self, client: NetworkClient, params: List[str]) -> ApiDataFetcher:
        pass


class MangaDexBookApiDataCreationStrategy(ApiDataCreationStartegy):

    def create(self, client: NetworkClient, params: List[str]) -> ApiDataFetcher:
        api_param = {
            "title": "Official color",
            "limit": "100",
            "order[createdAt]": "asc",
        }
        return MangaDexApiDataFetcher(
            client,
            f"manga",
            api_param,
        )


class MangaDexChapterFeedApiDataCreationStrategy(ApiDataCreationStartegy):

    def create(self, client: NetworkClient, params: List[str]) -> ApiDataFetcher:
        api_param = {"order[createdAt]": "asc", "limit": "500"}
        if len(params) == 0:
            raise Exception("At least, the book id must be defined in parameter")
        book_id = params[0]
        return MangaDexApiDataFetcher(
            client,
            f"manga/{book_id}/feed",
            api_param,
        )


class MangaDexApiDataFetcherFactory(ApiDataFetcherFactory):
    _creation_strategies: Dict[str, ApiDataCreationStartegy]
    _network_client: NetworkClient

    def __init__(self, client):
        self._network_client = client
        self._creation_strategies = {
            "book": MangaDexBookApiDataCreationStrategy(),
            "chapter_feed": MangaDexChapterFeedApiDataCreationStrategy(),
        }

    def create(self, type_name: str, params: List[str] = []):
        if not type_name in self._creation_strategies:
            raise Exception(f"{type_name} not found in the the MangaDexApiDataFactory")
        return self._creation_strategies[type_name].create(self._network_client, params)
