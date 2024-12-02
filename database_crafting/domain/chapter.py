from typing import Dict


class ChapterInfo:

    def __init__(self, volume_nbr: int, chapter_nbr: int, translated_language: str):
        self.volume_nbr = volume_nbr
        self.chapter_nbr = chapter_nbr
        self.translated_language = translated_language


class ChapterInstance:

    def __init__(self, id, manga_id):
        self.id = id
        self.manga_id = manga_id


class Chapter:

    def __init__(self, chapter_instance: ChapterInstance, chapter_info: ChapterInfo):
        self.chapter_instance = chapter_instance
        self.chapter_info = chapter_info


class ChapterPaired:

    def __init__(
        self,
        id: str,
        monochrome_chapter: ChapterInstance,
        chromatic_chapter: ChapterInstance,
        info: ChapterInfo,
    ):
        self.id = id
        self.monochrome_chapter = monochrome_chapter
        self.chromatic_chapter = chromatic_chapter
        self.info = info
