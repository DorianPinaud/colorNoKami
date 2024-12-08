from database_crafting.chapter.interfaces import ChapterRepository

from database_crafting.domain.chapter import Chapter

from pymongo.database import Database

from typing import List


class MongoChapterRepository(ChapterRepository):

    def __init__(self, db: Database):
        self._db = db

    def get_chapters(self) -> List[Chapter]:
        if self._db.chapters == None:
            raise Exception("chapters collection should exist in db at this point")
        return [
            Chapter(
                record["_id"],
                record["manga_id"],
                int(record["volume"]),
                int(record["chapter"]),
                record["translatedLanguage"],
            )
            for record in self._db.chapters.find({})
        ]

    def get_chapters_count(self) -> int:
        if self._db.chapters == None:
            raise Exception("chapters collection should exist in db at this point")
        return self._db.chapters.count_documents({})
