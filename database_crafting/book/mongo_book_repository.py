from database_crafting.book.interfaces import BookRepository
from database_crafting.api_data_fetcher.interfaces import ApiDataFetcherFactory

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from typing import Union, List, cast


from database_crafting.domain.book import Book


class MongoBookRepository(BookRepository):

    def __init__(self, db: Database):
        self._db = db

    def get_books(self) -> List[Book]:
        if self._db.books == None:
            raise Exception("book collection should exist in db at this point")
        return [Book.create_book(book) for book in self._db.books.find({})]

    def get_books_count(self) -> int:
        if self._db.books == None:
            raise Exception("book collection should exist in db at this point")
        return self._db.books.count_documents({})

    def pair_chapter_by_book(self) -> None:
        if self._db.books == None:
            raise Exception("book collection should exist in db at this point")
        if self._db.chapters == None:
            raise Exception("chapters collection should exist in db at this point")
        self._db.books.aggregate(
            [
                {
                    "$lookup": {
                        "from": "chapters",
                        "let": {
                            "full_color_book_id": "$_id",
                            "monochrome_book_id": "$monochrome_id",
                            "book_title": "$title",
                        },
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$or": [
                                            {
                                                "$eq": [
                                                    "$$full_color_book_id",
                                                    "$manga_id",
                                                ]
                                            },
                                            {
                                                "$eq": [
                                                    "$$monochrome_book_id",
                                                    "$manga_id",
                                                ]
                                            },
                                        ]
                                    }
                                }
                            },
                            {
                                "$group": {
                                    "_id": {
                                        "$concat": [
                                            "$volume",
                                            " - ",
                                            "$chapter",
                                            " - ",
                                            "$translatedLanguage",
                                        ]
                                    },
                                    "volume": {"$first": "$volume"},
                                    "chapter": {"$first": "$chapter"},
                                    "translatedLanguage": {
                                        "$first": "$translatedLanguage"
                                    },
                                    "chapter_version": {
                                        "$push": {
                                            "id": "$_id",
                                            "is_fullcolor": {
                                                "$expr": {
                                                    "$cond": {
                                                        "if": {
                                                            "$eq": [
                                                                "$$full_color_book_id",
                                                                "$manga_id",
                                                            ]
                                                        },
                                                        "then": True,
                                                        "else": False,
                                                    }
                                                }
                                            },
                                        }
                                    },
                                },
                            },
                            {
                                "$match": {
                                    "$and": [
                                        {
                                            "chapter_version": {
                                                "$elemMatch": {"is_fullcolor": True}
                                            }
                                        },
                                        {
                                            "chapter_version": {
                                                "$elemMatch": {"is_fullcolor": False}
                                            }
                                        },
                                    ]
                                },
                            },
                        ],
                        "as": "chapters",
                    },
                },
                {"$unwind": {"path": "$chapters"}},
                {
                    "$match": {
                        "$and": [
                            {"title": {"$ne": None}},
                            {"chapters._id": {"$ne": None}},
                            {"chapters.chapter_version": {"$size": 2}},
                        ]
                    }
                },
                {
                    "$project": {
                        "_id": {"$concat": ["$title", "$chapters._id"]},
                        "full_color_id": "$_id",
                        "monochrome_id": "$monochrome_id",
                        "title": "$title",
                        "chapter_info": {
                            "id": "$chapters._id",
                            "volume": "$chapters.volume",
                            "chapter": "$chapters.chapter",
                            "translatedLanguage": "$chapters.translatedLanguage",
                            "chapter_version": {
                                "$sortArray": {
                                    "input": "$chapters.chapter_version",
                                    "sortBy": {"is_fullcolor": -1},
                                }
                            },
                        },
                    }
                },
                {"$out": "chapters_paired"},
            ]
        )
