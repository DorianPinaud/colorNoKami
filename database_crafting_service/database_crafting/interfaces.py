from abc import ABC, abstractmethod

from typing import List


class DatabaseCraftingStage(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass


class DatabaseCraftingPipeline(ABC):

    @abstractmethod
    def get_stages(self) -> List[DatabaseCraftingStage]:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
