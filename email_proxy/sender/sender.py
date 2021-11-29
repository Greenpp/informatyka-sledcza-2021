import logging
from smtplib import SMTP

from email_proxy.sender.loader import EmailLoader

from ..settings import EMAILS_FILE, PROXY_HOST, PROXY_PORT

logger = logging.getLogger(__name__)


class EmailSender:
    """Email sender

    Sends loaded emails using SMTP protocol
    """

    def __init__(self) -> None:
        """Creates new instance of sender and initializes email loader"""
        self.loader = EmailLoader(EMAILS_FILE)

    def load_emails(self) -> None:
        """Loads emails with loader"""
        self.emails = self.loader.load_emails()
        logger.info(f'Loaded {len(self.emails)} emails')

    def send_emails(self):
        """Sends all loaded emails"""
        with SMTP(PROXY_HOST, PROXY_PORT) as client:
            logger.info(f'Sending emails to {PROXY_HOST}:{PROXY_PORT}')
            for email in self.emails:
                logger.info(f'Sending {email}')
                client.sendmail(
                    from_addr=email.sender,
                    to_addrs=email.receiver,
                    msg=email.generate_mime().as_string(),
                )
