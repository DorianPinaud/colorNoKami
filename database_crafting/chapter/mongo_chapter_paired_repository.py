from database_crafting.chapter.interfaces import ChapterPairedRepository

from database_crafting.domain.chapter import (
    ChapterPaired,
    ChapterInstance,
    ChapterInfo,
)

from pymongo.database import Database

from typing import List


class MongoChapterPairedRepository(ChapterPairedRepository):

    def __init__(self, db: Database):
        self._db = db

    def get_chapters_paired(self) -> List[ChapterPaired]:
        if self._db.chapters_paired == None:
            raise Exception(
                "chapters_paired collection should exist in db at this point"
            )
        return [
            ChapterPaired(
                record["_id"],
                ChapterInstance(
                    record["chapter_info"]["chapter_version"][1]["id"],
                    record["monochrome_id"],
                ),
                ChapterInstance(
                    record["chapter_info"]["chapter_version"][0]["id"],
                    record["full_color_id"],
                ),
                ChapterInfo(
                    record["chapter_info"]["volume"],
                    record["chapter_info"]["chapter"],
                    record["chapter_info"]["translatedLanguage"],
                ),
            )
            for record in self._db.chapters_paired.find({})
        ]

    def get_chapters_paired_count(self) -> int:
        if self._db.chapters_paired == None:
            raise Exception(
                "chapters_paired collection should exist in db at this point"
            )
        return self._db.chapters_paired.count_documents({})
