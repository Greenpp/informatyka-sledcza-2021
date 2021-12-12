import json
import logging
from pathlib import Path

from ..email import Email
from ..settings import ATTACHMENTS_DIR, EMAILS_FILE

logger = logging.getLogger(__name__)


class EmailLoader:
    """Email loader

    Loads emails form json file
    """

    def __init__(self, emails_file: str = EMAILS_FILE) -> None:
        """Creates a new email loader

        Args:
            emails_file (str): Path to the emails json file

        Raises:
            FileNotFoundError: If emails file does not exist
        """
        self.email_file_path = Path(emails_file)

        if self.email_file_path.exists():
            logging.debug(f'Found emails file')
        else:
            raise FileNotFoundError(
                f'Emails file not found at {self.email_file_path.absolute()}'
            )

    def load_emails(self) -> list[Email]:
        """Loads emails from file to list of Email objects

        Returns:
            list[Email]: List of Email objects
        """
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
                    [self._load_file(a) for a in email_data['attachments']],
                )

                emails.append(email)

        return emails

    def _load_file(self, f_name: str) -> tuple[str, bytes]:
        file_path = Path(ATTACHMENTS_DIR) / f_name

        if not file_path.exists():
            raise FileNotFoundError(
                f'Attachment file not found at {file_path.absolute()}'
            )

        with open(file_path, 'rb') as f:
            content = f.read()

        return f_name, content
