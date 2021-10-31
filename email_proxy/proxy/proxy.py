import asyncio
import logging

from aiosmtpd.controller import Controller
from email_proxy.settings import PROXY_HOST, PROXY_PORT

from .handler import AnalyzingProxy

logger = logging.getLogger(__name__)


class EmailProxy:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        logger.debug('Created event loop')

    def run(self) -> None:
        logger.debug('Starting proxy')
        self.loop.create_task(self._create_controller())
        self.loop.run_forever()

    async def _create_controller(self) -> None:
        controller = Controller(
            AnalyzingProxy,
            hostname=PROXY_HOST,
            port=PROXY_PORT,
        )
        controller.start()
