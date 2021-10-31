import asyncio
import logging

from aiosmtpd.controller import Controller

from .handler import Handler

logger = logging.getLogger(__name__)


class SMTPServer:
    def __init__(self, handler: Handler, hostname: str, port: int) -> None:
        self._handler = handler
        self._hostname = hostname
        self._port = port

        self._loop = asyncio.get_event_loop()
        logger.debug('Created event loop')

    def run(self) -> None:
        logger.debug('Starting server')
        self._loop.create_task(self._create_controller())
        self._loop.run_forever()

    async def _create_controller(self) -> None:
        controller = Controller(
            self._handler,
            hostname=self._hostname,
            port=self._port,
        )
        controller.start()
