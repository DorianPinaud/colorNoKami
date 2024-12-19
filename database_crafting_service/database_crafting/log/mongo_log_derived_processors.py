from database_crafting.log.interface import LogDerivedDataProcessor

from pymongo.database import Database


import re


class MongoLogDerivedChapters(LogDerivedDataProcessor):

    def __init__(self, db: Database):
        self._db = db

    def derived(self) -> None:
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


class MongoLogDerivedBooks(LogDerivedDataProcessor):

    def __init__(self, db: Database):
        self._db = db

    def derived(self) -> None:
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


class MongoLogDerivedScansUrls(LogDerivedDataProcessor):

    def __init__(self, db: Database):
        self._db = db

    def derived(self) -> None:
        self._db.log.aggregate(
            [
                {
                    "$match": {
                        "_id": {
                            "$regex": "https\:\/\/api.mangadex.org\/at-home\/server\/(.*)\/?"
                        },
                    },
                },
                {
                    "$addFields": {
                        "returnMatch": {
                            "$regexFind": {
                                "input": "$_id",
                                "regex": "https\:\/\/api.mangadex.org\/at-home\/server\/(.*)\/?",
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "id": {"$arrayElemAt": ["$returnMatch.captures", 0]},
                        "baseUrl": 1,
                        "hash": "$chapter.hash",
                        "url": "$chapter.data",
                    }
                },
                {"$out": "scans_urls"},
            ]
        )
