from typing import Dict


class Book:

    fullcolor_id: str
    monochrome_id: str
    title: str

    def __init__(self, fullcolor_id, monochrome_id, title):
        self.fullcolor_id = fullcolor_id
        self.monochrome_id = monochrome_id
        self.title = title

    @staticmethod
    def create_book(data: Dict):
        return Book(data["_id"], data["monochrome_id"], data["title"])
