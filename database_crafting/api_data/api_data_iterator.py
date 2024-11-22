from abc import ABC, abstractmethod
from typing import Dict, List, Type
from database_crafting.network_client.interface import NetworkClient
from urllib.parse import urlencode


class ApiDataIterator:

    _client: NetworkClient
    _offset: int
    _total: int
    _api_url: str
    _params: Dict
    _data: List
    _index: int
    _finish_pulling: bool

    def __init__(self, client, api_url, params={}):
        self._client = client
        self._offset = 0
        self._total = 0
        self._api_url = api_url
        self._params = params
        self._data = []
        self._index = 0
        self._finish_pulling = False
        self._reload_cache()

    def _reload_cache(self):

        if len(self._data) <= (self._index + 1):
            self._params["offset"] = self._offset
            url = f"{self._api_url}?{urlencode(self._params)}"
            data_json = self._client.get(url)
            self._offset += len(data_json["data"])
            self._total = data_json["total"]
            self._data = data_json["data"]
            self._index = 0
            if self._offset >= self._total:
                self._finish_pulling = True

    def value(self) -> Dict:
        return self._data[self._index]

    def __next__(self) -> None:
        self._reload_cache()
        self._index += 1
        if self._finish_pulling and self._index >= len(self._data):
            raise StopIteration()
        return self._data[self._index]
