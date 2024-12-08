from database_crafting.log.interface import LogDerivedDataProcessor

from pymongo.database import Database


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
