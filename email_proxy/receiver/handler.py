import logging

from ..handler import Handler

logger = logging.getLogger(__name__)


class ReceiverHandler(Handler):
    async def handle_DATA(self, server, session, envelope) -> str:
        logger.info(f'Data received in receiver')

        return '250 OK'
