import logging
from smtplib import SMTP

from aiosmtpd.smtp import Envelope

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
from .report import ReportGenerator

logger = logging.getLogger(__name__)


class AnalyzingProxyHandler(Handler):
    """Handler for proxy server"""
    
    def __init__(self) -> None:
        """Sets filter list and prepares report directory"""
        
        self._filters: list[Filter] = [
            KeywordsFilter(),
            RBLFilter(),
            VirusTotalFilter(),
        ]
        self.analyzed_emails = 0
        self.report_generator = ReportGenerator()

    async def handle_DATA(self, server, session, envelope) -> str:
        """Handles email data received by the smtp  server. Depending on filtering
        results, sends an email either to quarantine or reciever client"""
        
        logger.info(f'Debug: {self.report_generator}')
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
            self.report_generator.generate_report()

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
