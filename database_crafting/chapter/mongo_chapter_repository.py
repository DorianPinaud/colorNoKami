from database_crafting.chapter.interfaces import ChapterRepository

from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory
from database_crafting.book.interfaces import BookRepository
from database_crafting.domain.chapter import Chapter, ChapterPaired

from pymongo.database import Database

from typing import List


class MongoChapterRepository(ChapterRepository):

    def __init__(self, db: Database):

        self._db = db

    def get_chapters(self) -> List[Chapter]:
        if self._db.chapters == None:
            raise Exception("chapters collection should exist in db at this point")
        return [
            Chapter.create_chapter(chapter) for chapter in self._db.chapters.find({})
        ]

    def get_chapters_count(self) -> int:
        if self._db.chapters == None:
            raise Exception("chapters collection should exist in db at this point")
        return self._db.chapters.count_documents({})

    def get_chapters_paired(self) -> List[ChapterPaired]:
        if self._db.chapters_paired == None:
            raise Exception(
                "chapters_paired collection should exist in db at this point"
            )
        return [
            ChapterPaired.create_chapter_paired(chapter)
            for chapter in self._db.chapters_paired.find({})
        ]

    def get_chapters_paired_count(self) -> int:
        if self._db.chapters_paired == None:
            raise Exception(
                "chapters_paired collection should exist in db at this point"
            )
        return self._db.chapters_paired.count_documents({})
