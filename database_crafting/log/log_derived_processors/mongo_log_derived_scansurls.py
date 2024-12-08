from database_crafting.log.interface import LogDerivedDataProcessor

from pymongo.database import Database

import re


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
