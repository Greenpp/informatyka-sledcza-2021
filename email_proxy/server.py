import asyncio
import logging

from aiosmtpd.controller import Controller

from .handler import Handler

logger = logging.getLogger(__name__)


class SMTPServer:
    def __init__(self, handler: Handler, hostname: str, port: int) -> None:
        """Creates new SMTP server

        Args:
            handler (Handler): Custom handler used for email processing
            hostname (str): Server hostname
            port (int): Server port
        """
        self._handler = handler
        self._hostname = hostname
        self._port = port

        self._loop = asyncio.get_event_loop()
        logger.info('Created event loop')

    def run(self) -> None:
        """Starts the server"""
        logger.info('Starting server')
        self._loop.create_task(self._create_controller())
        self._loop.run_forever()

    async def _create_controller(self) -> None:
        """Creates the controller"""
        controller = Controller(
            self._handler,
            hostname=self._hostname,
            port=self._port,
        )
        controller.start()
