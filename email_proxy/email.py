from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


@dataclass
class Email:
    sender: str
    receiver: str
    subject: str
    msg: str
    attachements: list[Path]

    def generate_mime(self) -> MIMEMultipart:
        message = MIMEMultipart()

        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = self.subject

        body = MIMEText(self.msg, 'plain')
        message.attach(body)

        for att_path in self.attachements:
            if not att_path.exists():
                raise FileNotFoundError(
                    f'Attachment at {att_path.absolute()} not found'
                )

            with open(att_path, 'rb') as f:
                att = MIMEBase('application', 'octet-stream')
                att.set_payload(f.read())

                encoders.encode_base64(att)

                att.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {att_path.name}',
                )
                message.attach(att)

        return message
