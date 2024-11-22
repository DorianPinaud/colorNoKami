from database_crafting.log.interface import LogRepository
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import time
from typing import Dict, Any


class MongoLogRepository(LogRepository):
    _timestamp: float
    _cache: Dict
    _db: Database
    _logs: Collection

    def __init__(self, db) -> None:
        self._db = db
        self._logs = self._db.log
        self._cache = {}
        self._timestamp = time.time()

    def is_logged(self, url: str) -> bool:
        return self._logs.find_one({"_id": url}) != None

    def register_log(self, url: str, data: Dict) -> None:
        self._cache[url] = data
        if (time.time() - self._timestamp) > 3:
            self._logs.insert_many([{"_id": k, **v} for k, v in self._cache.items()])
            self._cache = {}
            self._timestamp = time.time()

    def get_log(self, url: str) -> Any:
        return self._logs.find_one({"_id": url})

    def count_log(self) -> int:

        return self._logs.count_documents({})
