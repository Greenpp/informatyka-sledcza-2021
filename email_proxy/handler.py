from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    async def handle_DATA(self, server, session, envelope) -> str:
        pass
