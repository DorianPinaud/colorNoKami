from __future__ import annotations
from typing import Dict, List, Union


class Chapter:

    def __init__(
        self,
        id: str,
        manga_id: str,
        volume_nbr: int,
        chapter_nbr: int,
        translated_language: str,
    ):
        self.id = id
        self.manga_id: str = ""
        self.volume_nbr: int = 0
        self.chapter_nbr: int = 0
        self.translated_language: str = ""


class ChapterPair:

    def __init__(
        self,
        id: str,
        monochrome_chapter: Chapter,
        chromatic_chapter: Chapter,
    ):
        self.id = id
        self.monochrome_chapter = monochrome_chapter
        self.chromatic_chapter = chromatic_chapter


class ScansUrls:

    def __init__(self, base_url: str, hash: str, urls: List[str]):
        self.base_url = base_url
        self.hash = hash
        self.scans_urls = urls


class ChapterWithScansUrls:

    def __init__(self, chapter: Chapter, scans_urls: ScansUrls):
        self.chapter = chapter
        self.scan_urls = scans_urls


class ChapterPairWithScansUrls:

    def __init__(
        self,
        id: str,
        monochrome_chapter: ChapterWithScansUrls,
        chromatic_chapter: ChapterWithScansUrls,
    ):
        self.id = id
        self.monochrome_chapter = monochrome_chapter
        self.chromatic_chapter = chromatic_chapter
