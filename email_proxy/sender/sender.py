import logging
from smtplib import SMTP

from email_proxy.sender.loader import EmailLoader

from ..settings import EMAILS_FILE, PROXY_HOST, PROXY_PORT

logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(self) -> None:
        self.loader = EmailLoader(EMAILS_FILE)

    def load_emails(self) -> None:
        self.emails = self.loader.load_emails()
        logger.info(f'Loaded {len(self.emails)} emails')

    def send_emails(self):
        with SMTP(PROXY_HOST, PROXY_PORT) as client:
            logger.info(f'Sending emails to {PROXY_HOST}:{PROXY_PORT}')
            for email in self.emails:
                logger.info(f'Sending {email}')
                client.sendmail(
                    from_addr=email.sender,
                    to_addrs=email.receiver,
                    msg=email.generate_mime().as_string(),
                )
