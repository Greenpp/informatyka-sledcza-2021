from abc import ABC, abstractmethod


class Handler(ABC):
    """Custom aiosmtpd handler"""

    @abstractmethod
    async def handle_DATA(self, server, session, envelope) -> str:
        """Handles email data received by the smtp  server

        Args:
            server (): Server
            session (): Session
            envelope (): Received data

        Returns:
            str: Response
        """
        pass
