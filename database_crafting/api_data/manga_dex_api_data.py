from database_crafting.api_data.interfaces import ApiData
from database_crafting.api_data.api_data_iterator import ApiDataIterator


class MangaDexApiData(ApiData):

    def __init__(self, client, api_url, params):
        self._iterator = ApiDataIterator(
            client, f"https://api.mangadex.org/{api_url}", params
        )

    def __iter__(self):
        return self._iterator

    def fetch(self):
        [_ for _ in self]
