from database_crafting.book.interfaces import BookRepository
from database_crafting.api_data.interfaces import ApiDataFactory
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Union, List
from database_crafting.domain.book import Book


class MongoBookRepository(BookRepository):
    _db: Database
    _logs_db_collec: Collection
    _books_db_collec: Union[Collection, None]

    def __init__(self, db: Database):
        self._db = db
        self._logs_db_collec = db.log
        self._books_db_collec = None

    def fetch_books(self, api_data_factory: ApiDataFactory):
        api_data = api_data_factory.create_api_data("book")
        api_data.fetch()
        self._logs_db_collec.aggregate(
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
        self._books_db_collec = self._db.books

    def get_books(self) -> List[Book]:
        if self._books_db_collec == None:
            raise Exception("MongoBookRepository instance should be init before")
        books = self._books_db_collec.find({})
        return [Book.create_book(book) for book in books]

    def get_books_count(self) -> int:
        if self._books_db_collec == None:
            raise Exception("MongoBookRepository instance should be init before")
        return self._books_db_collec.count_documents({})
