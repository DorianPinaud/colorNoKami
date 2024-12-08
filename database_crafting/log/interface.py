from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Dict


class LogRepository(ABC):

    @abstractmethod
    def is_logged(self, url: str) -> bool:
        pass

    @abstractmethod
    def register_log(self, url: str, data: Dict):
        pass

    @abstractmethod
    def get_log(self, url: str) -> Dict:
        pass

    @abstractmethod
    def count_log(self) -> int:
        pass


class LogDerivedDataProcessor(ABC):

    @abstractmethod
    def derived(self) -> None:
        pass
