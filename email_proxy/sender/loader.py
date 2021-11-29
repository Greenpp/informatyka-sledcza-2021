import json
import logging
from pathlib import Path

from ..email import Email

logger = logging.getLogger(__name__)


class EmailLoader:
    def __init__(self, emails_file: str) -> None:
        self.email_file_path = Path(emails_file)

        if self.email_file_path.exists():
            logging.debug(f'Found emails file')
        else:
            raise FileNotFoundError(
                f'Emails file not found at {self.email_file_path.absolute()}'
            )

    def load_emails(self) -> list[Email]:
        with open(self.email_file_path, 'rb') as f:
            data = json.load(f)

        emails = []
        for email_data in data:
            for receiver in email_data['receivers']:
                email = Email(
                    email_data['sender'],
                    receiver,
                    email_data['subject'],
                    email_data['message'],
                    [Path(a) for a in email_data['attachements']],
                )

                emails.append(email)

        return emails
