from database_crafting.api_data_fetcher.interfaces import ApiDataFetcher
from database_crafting.network_client.interface import NetworkClient
from urllib.parse import urlencode

from typing import Dict


class MangaDexApiDataFetcher(ApiDataFetcher):

    def __init__(self, client: NetworkClient, api_url: str, params: Dict = {}):
        self._client = client
        self._api_url = api_url
        self._params = params

    def fetch(self):
        url = f"https://api.mangadex.org/{self._api_url}?{urlencode(self._params)}"
        self._client.get(url)
