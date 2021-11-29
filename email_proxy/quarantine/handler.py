import logging

from ..handler import Handler

logger = logging.getLogger(__name__)


class QuarantineHandler(Handler):
    async def handle_DATA(self, server, session, envelope) -> str:
        logger.info(f'Data received in quarantine')
        
        return '250 OK'
