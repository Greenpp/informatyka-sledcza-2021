from sqlalchemy import or_

from ..db import Attachment, Email, session_factory


class ReportGenerator:
    def generate_report(self):
        session = session_factory()

        total_emails = session.query(Email).count()
        dangerous_emails = (
            session.query(Email)
            .join(Email.attachments)
            .filter(or_(Email.is_dangerous == True, Attachment.is_dangerous == True))
            .distinct(Email.id)
            .count()
        )
        safe_emails = total_emails - dangerous_emails

        total_attachments = session.query(Attachment).count()
        dangerous_attachments = (
            session.query(Attachment).filter(Attachment.is_dangerous).count()
        )
        safe_attachments = total_attachments - dangerous_attachments

        # TODO change form of the report
        print(
            f'Total emails: {total_emails}\nDangerous emails: {dangerous_emails}\nSafe emails: {safe_emails}'
        )
        print(
            f'Total attachments: {total_attachments}\nDangerous attachments: {dangerous_attachments}\nSafe attachments: {safe_attachments}'
        )

        session.close()
