import logging
from smtplib import SMTP

from aiosmtpd.smtp import Envelope
from email_proxy.proxy.report import ReportGenerator

from ..email import Email
from ..handler import Handler
from ..settings import (
    QUARANTINE_HOST,
    QUARANTINE_PORT,
    REPORTING_EVERY_N_EMAILS,
    TARGET_HOST,
    TARGET_PORT,
)
from .filters.filter import Filter
from .filters.keywords import KeywordsFilter
from .filters.rbl import RBLFilter
from .filters.virus_total import VirusTotalFilter

logger = logging.getLogger(__name__)


class AnalyzingProxyHandler(Handler):
    _filters: list[Filter] = [
        # TODO uncomment for production
        # RBLFilter(),
        # VirusTotalFilter(),
        # KeywordsFilter()
    ]
    analyzed_emails = 0

    async def handle_DATA(self, server, session, envelope) -> str:
        logger.info(f'Data received in proxy')
        email = Email.from_envelope(envelope)
        logger.info(f'{email=}')

        dangerous = False
        for f in self._filters:
            if f.is_spam_or_dangerous(email):
                dangerous = True
                break
                
        if dangerous:
            logger.info('Sending email to quarantine')
            self._send_to_quarantine(envelope)
        else:
            logger.info('Sending email to receiver')
            self._send_to_receiver(envelope)

        email.save_to_db(dangerous)
        
        self.analyzed_emails += 1
        if self.analyzed_emails % REPORTING_EVERY_N_EMAILS == 0:
            report_generator = ReportGenerator()
            report_generator.generate_report()

        return '250 OK'

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
