from database_crafting.chapter.interfaces import ChapterPairRepository

from database_crafting.domain.chapter import ChapterPair, Chapter

from pymongo.database import Database

from typing import List


class MongoChapterPairRepository(ChapterPairRepository):

    def __init__(self, db: Database):
        self._db = db

    def get_chapters_pair(self) -> List[ChapterPair]:
        if self._db.chapter_pair == None:
            raise Exception(
                "chapters_pair_with_scans_urls collection should exist in db at this point"
            )
        return [
            ChapterPair(
                record["_id"],
                Chapter(
                    record["chapter_monochrome"],
                    record["monochrome_manga_id"],
                    int(record["volume"]),
                    int(record["chapter_nbr"]),
                    record["translatedLanguage"],
                ),
                Chapter(
                    record["chapter_fullcolor"],
                    record["full_color_manga_id"],
                    int(record["volume"]),
                    int(record["chapter_nbr"]),
                    record["translatedLanguage"],
                ),
            )
            for record in self._db.chapters_pair.find({})
        ]

    def get_chapters_pair_count(self) -> int:
        if self._db.chapters_pair == None:
            raise Exception("chapters_pair collection should exist in db at this point")
        return self._db.chapters_pair.count_documents({})
