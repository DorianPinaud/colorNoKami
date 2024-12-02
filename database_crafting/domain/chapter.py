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
            int(data["volume"]),
            int(data["chapter"]),
            data["translatedLanguage"],
        )


class ChapterVersion:
    id: str
    is_fullcolor: bool

    def __init__(self, id, is_fullcolor):
        return ChapterVersion(id, is_fullcolor)

    @staticmethod
    def create_chapter_version(data: Dict):
        return ChapterVersion(data["id"], data["is_fullcolor"])


class ChapterInfo:
    volume_nbr: int
    chapter_nbr: float
    translated_language: str
    chapter_version: ChapterVersion

    def __init__(self, volume_nbr, chapter_nbr, translated_language, chapter_version):
        self.volume_nbr = volume_nbr
        self.chapter_version = chapter_version
        self.translated_language = translated_language
        self.chapter_version = chapter_version

    @staticmethod
    def create_chapter_info(data: Dict):
        return ChapterInfo(
            int(data["volume"]),
            float(data["chapter"]),
            data["translatedLanguage"],
            ChapterVersion.create_chapter_version(data),
        )


class ChapterPaired:
    id: str
    full_color_id: str
    monochrome_id: str
    title: str
    chapter_info: ChapterInfo

    def __init__(self, id, full_color_id, monochrome_id, title, chapter_info):
        self.id = id
        self.full_color_id = full_color_id
        self.monochrome_id = monochrome_id
        self.title = title
        self.chapter_info = chapter_info

    @staticmethod
    def create_chapter_paired(data: Dict):
        return Chapter(
            data["_id"],
            data["full_color_id"],
            data["monochrome_id"],
            data["title"],
            ChapterInfo.create_chapter_info(data),
        )
