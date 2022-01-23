import logging
from dataclasses import dataclass
from email import encoders, message_from_bytes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from aiosmtpd.smtp import Envelope

from .db import Email as DBEmail
from .db import session_factory

logger = logging.getLogger(__name__)


@dataclass
class Email:
    """Email representation"""

    sender: str
    receiver: str
    subject: str
    msg: str
    attachments: list[tuple[str, bytes]]

    db_id: Optional[int] = None

    def generate_mime(self) -> MIMEMultipart:
        """Generates email MIME object

        Raises:
            FileNotFoundError: If attachment file does not exist

        Returns:
            MIMEMultipart: MIME object
        """
        message = MIMEMultipart()

        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = self.subject

        body = MIMEText(self.msg, 'plain')
        message.attach(body)

        for f_name, f_content in self.attachments:
            att = MIMEBase('application', 'octet-stream')
            att.set_payload(f_content)
            encoders.encode_base64(att)
            att.add_header(
                'Content-Disposition',
                f'attachment; filename={f_name}',
            )

            message.attach(att)

        return message

    @classmethod
    def from_envelope(cls, envelope: Envelope) -> 'Email':
        message = message_from_bytes(envelope.original_content)

        sender = message['From']
        receiver = message['To']
        subject = message['Subject']

        body = ''
        attachments = []
        for p in message.get_payload():
            content_type = p.get_content_type()
            if content_type == 'text/plain':
                body = p.get_payload()
            elif content_type == 'application/octet-stream':
                att = p.get_payload(decode=True)
                f_name = p._headers[-1][1].split('=')[1]
                attachments.append((f_name, att))
            else:
                logger.warning(f'Unknown content type, {content_type=}')

        return cls(
            sender=sender,
            receiver=receiver,
            subject=subject,
            msg=body,
            attachments=attachments,
        )

    def save_to_db(self, dangerous: bool) -> None:
        db_email = DBEmail(
            sender=self.sender,
            receiver=self.receiver,
            subject=self.subject,
            msg=self.msg,
            is_dangerous=dangerous,
        )

        session = session_factory()
        session.add(db_email)
        session.commit()

        self.db_id = db_email.id

        session.close()
        logger.info('Message saved to DB')
