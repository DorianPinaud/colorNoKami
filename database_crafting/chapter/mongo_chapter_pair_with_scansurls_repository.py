from database_crafting.chapter.interfaces import ChapterPairWithScansUrlsRepository

from database_crafting.domain.chapter import (
    ChapterPairWithScansUrls,
    ChapterWithScansUrls,
    Chapter,
    ScansUrls,
)

from pymongo.database import Database

from typing import List


class MongoChapterPairWithScansUrlsRepository(ChapterPairWithScansUrlsRepository):

    def __init__(self, db: Database):
        self._db = db

    def get_chapter_pair_with_scans_urls(self) -> List[ChapterPairWithScansUrls]:
        if self._db.chapters_pair_with_scans_urls == None:
            raise Exception(
                "chapters_pair_with_scans_urls collection should exist in db at this point"
            )
        return [
            ChapterPairWithScansUrls(
                record["_id"],
                ChapterWithScansUrls(
                    Chapter(
                        record["chapter_monochrome"]["id"],
                        record["monochrome_manga_id"],
                        int(record["volume"]),
                        int(record["chapter_nbr"]),
                        record["translatedLanguage"],
                    ),
                    ScansUrls(
                        record["chapter_monochrome"]["base_url"],
                        record["chapter_monochrome"]["hash"],
                        record["chapter_monochrome"]["urls"],
                    ),
                ),
                ChapterWithScansUrls(
                    Chapter(
                        record["chapter_fullcolor"]["id"],
                        record["full_color_manga_id"],
                        int(record["volume"]),
                        int(record["chapter_nbr"]),
                        record["translatedLanguage"],
                    ),
                    ScansUrls(
                        record["chapter_fullcolor"]["base_url"],
                        record["chapter_fullcolor"]["hash"],
                        record["chapter_fullcolor"]["urls"],
                    ),
                ),
            )
            for record in self._db.chapters_pair_with_scans_urls.find({})
        ]

    def get_chapters_pair_with_scans_urls_count(self) -> int:
        if self._db.chapters_pair_with_scans_urls == None:
            raise Exception(
                "chapters_pair_with_scans_urls collection should exist in db at this point"
            )
        return self._db.chapters_pair_with_scans_urls.count_documents({})
