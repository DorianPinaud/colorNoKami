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
