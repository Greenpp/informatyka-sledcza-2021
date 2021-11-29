import logging
from smtplib import SMTP

from ..handler import Handler
from ..settings import (
    QUARANTINE_HOST,
    QUARANTINE_PORT,
    TARGET_HOST,
    TARGET_PORT,
)

logger = logging.getLogger(__name__)


class AnalyzingProxyHandler(Handler):
    async def handle_DATA(self, server, session, envelope) -> str:
        logger.info(f'Data received in proxy')

        logger.info('Sending email to receiver')
        self._send_to_receiver(envelope)
        logger.info('Sending email to quarantine')
        self._send_to_quarantine(envelope)

        return '250 OK'

    def _send_to_receiver(self, envelope) -> None:
        """Sends email to the receiver.

        Args:
            envelope (): Email data
        """
        with SMTP(TARGET_HOST, TARGET_PORT) as client:
            client.sendmail(
                envelope.mail_from,
                envelope.rcpt_tos,
                envelope.original_content,
            )

    def _send_to_quarantine(self, envelope) -> None:
        """Sends email to the quarantine

        Args:
            envelope (): Email data
        """
        with SMTP(QUARANTINE_HOST, QUARANTINE_PORT) as client:
            client.sendmail(
                envelope.mail_from,
                envelope.rcpt_tos,
                envelope.original_content,
            )
