from database_crafting.chapter.interfaces import EnrichChaptersPairwithScansUrlsService

from pymongo.database import Database


class MongoEnrichChaptersPairwithScansUrlsService(
    EnrichChaptersPairwithScansUrlsService
):

    def __init__(self, db: Database):
        self._db = db

    def enrich(self):
        if self._db.chapters_pair == None:
            raise Exception("chapters_pair collection should exist in db at this point")
        if self._db.scans_urls == None:
            raise Exception("scans_urls collection should exist in db at this point")
        self._db.chapters_pair.aggregate(
            [
                {
                    "$lookup": {
                        "from": "scans_urls",
                        "foreignField": "id",
                        "localField": "chapter_fullcolor",
                        "as": "scans_urls",
                    }
                },
                {
                    "$unwind": {
                        "path": "$scans_urls",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {"$set": {"chapter_fullcolor": "$scans_urls"}},
                {"$unset": ["scans_urls", "chapter_fullcolor._id"]},
                {"$out": "chapters_pair_with_scans_urls"},
            ]
        )
        self._db.chapters_pair_with_scans_urls.aggregate(
            [
                {
                    "$lookup": {
                        "from": "scans_urls",
                        "foreignField": "id",
                        "localField": "chapter_monochrome",
                        "as": "scans_urls",
                    }
                },
                {
                    "$unwind": {
                        "path": "$scans_urls",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {"$set": {"chapter_monochrome": "$scans_urls"}},
                {"$unset": ["scans_urls", "chapter_monochrome._id"]},
                {"$out": "chapters_pair_with_scans_urls"},
            ]
        )
