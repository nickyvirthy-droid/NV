from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ):
        pass

    @abstractmethod
    async def health(self):
        pass

    @abstractmethod
    def name(self):
        pass
