import logging

from ..email import Email
from ..handler import Handler

logger = logging.getLogger(__name__)


class ReceiverHandler(Handler):
    async def handle_DATA(self, server, session, envelope) -> str:
        email = Email.from_envelope(envelope)
        logger.info(f'Data received in receiver | {email=}')

        return '250 OK'
