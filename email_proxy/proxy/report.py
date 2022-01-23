import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import or_

from ..db import Attachment, Email, session_factory
from ..settings import REPORT_DIR

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self) -> None:
        """Prepares directory"""
        
        self._prepare_report_dir()

    def _prepare_report_dir(self):
        """Creates a directory for the report to be saved"""
        
        report_dir = Path(REPORT_DIR)
        report_dir.mkdir(exist_ok=True, parents=True)

        self.report_dir = report_dir
        logger.info(f'Using reports directory {self.report_dir.absolute()}')

    def generate_report(self):
        """Generates report containing a number of safe and dangerous
        mail/attachments received by proxy server"""
        
        logger.info('Generating report')
        session = session_factory()

        total_emails = session.query(Email).count()
        dangerous_emails = (
            session.query(Email)
            .outerjoin(Attachment)
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

        session.close()

        report_file = self.report_dir / f'report-{total_emails}-{datetime.now()}.txt'
        with open(report_file, 'w') as f:
            f.write(
                f'Total emails: {total_emails}\nDangerous emails: {dangerous_emails}\nSafe emails: {safe_emails}'
            )
            f.write('\n')
            f.write(
                f'Total attachments: {total_attachments}\nDangerous attachments: {dangerous_attachments}\nSafe attachments: {safe_attachments}'
            )
