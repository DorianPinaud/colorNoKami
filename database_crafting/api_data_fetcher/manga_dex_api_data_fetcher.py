from database_crafting.api_data_fetcher.interfaces import ApiDataFetcher
from database_crafting.network_client.interface import NetworkClient
from urllib.parse import urlencode

from typing import Dict


class MangaDexApiDataFetcher(ApiDataFetcher):

    _client: NetworkClient
    _api_url: str
    _params: Dict

    def __init__(self, client, api_url, params):
        self._client = client
        self._api_url = api_url
        self._params = params

    def _run_partial_fetching(self, offset: int):
        self._params["offset"] = offset
        url = f"https://api.mangadex.org/{self._api_url}?{urlencode(self._params)}"
        data_json = self._client.get(url)
        return data_json["total"], len(data_json["data"]), data_json["data"]

    def fetch(self):
        offset_records = 0
        total_records, offset_records, records = self._run_partial_fetching(
            offset_records
        )
        while offset_records < total_records:
            total_records, nbr_records, records = self._run_partial_fetching(
                offset_records
            )
            offset_records += nbr_records
