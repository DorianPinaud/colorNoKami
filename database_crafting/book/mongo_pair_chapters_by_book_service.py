from database_crafting.book.interfaces import PairChaptersBybookService

from pymongo.database import Database


class MongoPairChaptersByBookService(PairChaptersBybookService):

    def __init__(self, db: Database):
        self._db = db

    def pairing(self) -> None:
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
                                        {"chapter_version": {"$size": 2}},
                                    ]
                                },
                            },
                            {
                                "$project": {
                                    "chapter": 1,
                                    "volume": 1,
                                    "translatedLanguage": 1,
                                    "chapter_version": {
                                        "$sortArray": {
                                            "input": "$chapter_version",
                                            "sortBy": {"is_fullcolor": -1},
                                        }
                                    },
                                }
                            },
                            {
                                "$project": {
                                    "chapter": 1,
                                    "volume": 1,
                                    "translatedLanguage": 1,
                                    "chapter_fullcolor": {
                                        "$arrayElemAt": ["$chapter_version", 0]
                                    },
                                    "chapter_monochrome": {
                                        "$arrayElemAt": ["$chapter_version", 1]
                                    },
                                }
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
                        ]
                    }
                },
                {
                    "$project": {
                        "_id": {"$concat": ["$title", "$chapters._id"]},
                        "title": "$title",
                        "volume": "$chapters.volume",
                        "chapter_nbr": "$chapters.chapter",
                        "translatedLanguage": "$chapters.translatedLanguage",
                        "monochrome_manga_id": "$monochrome_id",
                        "full_color_manga_id": "$_id",
                        "chapter_fullcolor": "$chapters.chapter_fullcolor.id",
                        "chapter_monochrome": "$chapters.chapter_monochrome.id",
                    }
                },
                {"$out": "chapters_pair"},
            ]
        )
