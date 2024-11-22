from typing import Dict


class Chapter:
    id: str
    manga_id: str
    volume_nbr: int
    chapter_nbr: int
    translated_language: str

    def __init__(self, id, manga_id, volume_nbr, chapter_nbr, translated_language):
        self.id = id
        self.manga_id = manga_id
        self.volume_nbr = volume_nbr
        self.chapter_nbr = chapter_nbr
        self.translated_language = translated_language

    @staticmethod
    def create_chapter(data: Dict):
        return Chapter(
            data["_id"],
            data["manga_id"],
            int(data["chapter"]),
            int(data["chapter"]),
            data["translatedLanguage"],
        )
