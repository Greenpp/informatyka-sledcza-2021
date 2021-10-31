import json
import logging
from dataclasses import dataclass
from pathlib import Path

from .settings import EMAILS_FILE

logger = logging.getLogger(__name__)


@dataclass
class Email:
    sender: str
    receivers: list[str]
    msg: str
    attachements: list[Path]


class EmailLoader:
    def __init__(self) -> None:
        self.emails = []
        self._load_emails()

        logging.debug(f'Loaded {len(self.emails)} emails')

    def _load_emails(self) -> None:
        with open(EMAILS_FILE, 'rb') as f:
            data = json.load(f)

        for email_data in data:
            email = Email(
                email_data['sender'],
                email_data['receiver'],
                email_data['msg'],
                [Path(a) for a in email_data['attachements']],
            )

            self.emails.append(email)

    def __iter__(self):
        yield from self.emails
