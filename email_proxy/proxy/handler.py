import logging
from smtplib import SMTP

from aiosmtpd.smtp import Envelope

from ..email import Email
from ..handler import Handler
from ..settings import (
    QUARANTINE_HOST,
    QUARANTINE_PORT,
    TARGET_HOST,
    TARGET_PORT,
)
from .filters.filter import Filter
from .filters.rbl import RBLFilter
from .filters.virus_total import VirusTotalFilter
from .filters.keywords import KeywordsFilter

logger = logging.getLogger(__name__)


class AnalyzingProxyHandler(Handler):
    _filters: list[Filter] = [
        # TODO uncomment for production
        # RBLFilter(),
        # VirusTotalFilter(),
        # KeywordsFilter()
    ]

    async def handle_DATA(self, server, session, envelope) -> str:
        RETURN_CODE = '250 OK'
        logger.info(f'Data received in proxy')
        email = Email.from_envelope(envelope)
        logger.info(f'{email=}')

        for f in self._filters:
            if f.is_spam_or_dangerous(email):
                logger.info('Sending email to quarantine')
                self._send_to_quarantine(envelope)
                return RETURN_CODE
        logger.info('Sending email to receiver')
        self._send_to_receiver(envelope)

        return RETURN_CODE

    def _send_to_receiver(self, envelope: Envelope) -> None:
        """Sends email to the receiver.

        Args:
            envelope (): Email data
        """
        self._pass(TARGET_HOST, TARGET_PORT, envelope)

    def _send_to_quarantine(self, envelope: Envelope) -> None:
        """Sends email to the quarantine

        Args:
            envelope (): Email data
        """
        self._pass(QUARANTINE_HOST, QUARANTINE_PORT, envelope)

    def _pass(self, host: str, port: int, envelope: Envelope) -> None:
        with SMTP(host, port) as client:
            client.sendmail(
                envelope.mail_from,
                envelope.rcpt_tos,
                envelope.original_content,
            )
