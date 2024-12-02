from database_crafting.log.interface import LogRepository
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import time
from typing import Dict, Any
import re


class MongoLogRepository(LogRepository):

    def __init__(self, db: Database) -> None:
        self._db = db
        self._cache: Dict = {}
        self._timestamp = time.time()

    def is_logged(self, url: str) -> bool:
        return self._db.log.find_one({"_id": url}) != None

    def register_log(self, url: str, data: Dict) -> None:
        self._cache[url] = data
        if (time.time() - self._timestamp) > 3:
            self._db.log.insert_many([{"_id": k, **v} for k, v in self._cache.items()])
            self._cache = {}
            self._timestamp = time.time()

    def get_log(self, url: str) -> Any:
        return self._db.log.find_one({"_id": url})

    def count_log(self) -> int:
        return self._db.log.count_documents({})

    def derived_book_from_logs(self) -> None:
        self._db.log.aggregate(
            [
                {"$unwind": {"path": "$data"}},
                {"$unwind": {"path": "$data.relationships"}},
                {
                    "$match": {
                        "data.relationships.type": "manga",
                        "data.relationships.related": "monochrome",
                    }
                },
                {
                    "$project": {
                        "_id": "$data.id",
                        "monochrome_id": "$data.relationships.id",
                        "title": "$data.attributes.title.en",
                    }
                },
                {
                    "$group": {
                        "_id": "$_id",
                        "monochrome_id": {"$first": "$monochrome_id"},
                        "title": {"$first": "$title"},
                    }
                },
                {"$out": "books"},
            ]
        )

    def derived_chapters_from_logs(self) -> None:
        valid_int_pattern = re.compile(r"^\d+$")
        self._db.log.aggregate(
            [
                {
                    "$match": {
                        "_id": {
                            "$regex": "https\:\/\/api.mangadex.org\/manga\/(.*)\/feed"
                        },
                        "data": {"$elemMatch": {"$ne": None}},
                    },
                },
                {"$unwind": "$data"},
                {
                    "$match": {
                        "data.attributes.chapter": {"$regex": "^\d+$"},
                        "data.attributes.volume": {"$regex": "^\d+$"},
                    }
                },
                {
                    "$addFields": {
                        "returnMatch": {
                            "$regexFind": {
                                "input": "$_id",
                                "regex": "https\:\/\/api.mangadex.org\/manga\/(.*)\/feed",
                            }
                        }
                    }
                },
                {"$unwind": "$returnMatch.captures"},
                {
                    "$project": {
                        "_id": "$data.id",
                        "manga_id": "$returnMatch.captures",
                        "volume": "$data.attributes.volume",
                        "chapter": "$data.attributes.chapter",
                        "title": "$data.attributes.title",
                        "translatedLanguage": "$data.attributes.translatedLanguage",
                    }
                },
                {
                    "$group": {
                        "_id": "$_id",
                        "manga_id": {"$first": "$manga_id"},
                        "volume": {"$first": "$volume"},
                        "chapter": {"$first": "$chapter"},
                        "translatedLanguage": {"$first": "$translatedLanguage"},
                    }
                },
                {"$out": "chapters"},
            ]
        )
