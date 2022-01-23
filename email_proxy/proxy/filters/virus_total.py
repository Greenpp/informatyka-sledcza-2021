import hashlib
import io
import logging
import time
from typing import Optional

import vt
from dotenv import dotenv_values

from ...db import Attachment
from ...db import Email as DBEmail
from ...db import session_factory
from ...email import Email
from ...settings import VT_JOIN_DELAY, VT_JOIN_RETRIES
from .filter import Filter

logger = logging.getLogger(__name__)


class VirusTotalFilter(Filter):
    def __init__(self) -> None:
        try:
            key = dotenv_values('.env')['VT_KEY']
        except Exception as e:
            raise Exception('Failed to load VirusTotal API key')

        self.vt_client = vt.Client(key)

    def _get_existing_scan_result(self, f_hash: str) -> Optional[bool]:
        try:
            result = self.vt_client.get_object(f'/files/{f_hash}')
        except vt.APIError as e:
            logger.info('Result not found')
            result = None

        return result

    def _enqueue_file_scan(self, file_content: bytes) -> str:
        io_content = io.BytesIO(file_content)
        status = self.vt_client.scan_file(io_content)

        return status.id

    def _is_dangerous_result(self, result) -> bool:
        verdict = result.last_analysis_stats
        return verdict['malicious'] or verdict['suspicious']

    def _join_results(self, ids: list[str]) -> dict[str, dict]:
        id_status = {id_: False for id_ in ids}

        results = {}
        for _ in range(VT_JOIN_RETRIES):
            for id_ in id_status.keys():
                if not id_status[id_]:
                    stat_obj = self.vt_client.get_object(f'/analyses/{id_}')
                    if stat_obj.status == 'completed':
                        results[id_] = stat_obj.stats
                        id_status[id_] = True
            if not all(id_status.values()):
                time.sleep(VT_JOIN_DELAY)

        return results

    def is_spam_or_dangerous(self, email: Email) -> bool:
        logger.info('Running VirusTotal filter')
        results = {}
        enqueued = []
        id_to_hash = {}
        for f_name, f_content in email.attachments:
            f_hash = hashlib.sha256(f_content).hexdigest()

            logger.info(f'Checking file {f_name} | {f_hash=}')
            existing_status = self._get_existing_scan_result(f_hash)
            if existing_status is not None:
                logger.info(f'File {f_name} result found')
                results[f_hash] = existing_status
            else:
                logger.info(f'File {f_name} result not found, scanning')
                try:
                    scan_id = self._enqueue_file_scan(f_content)
                    id_to_hash[scan_id] = f_hash
                    enqueued.append(scan_id)
                except Exception as e:
                    logger.warning(f'Failed to scan file {f_name} | {e=}')

        logger.info('Joining results')
        scan_results = self._join_results(enqueued)
        scan_results_translated = {
            id_to_hash[id_]: res for id_, res in scan_results.items()
        }
        statuses = scan_results_translated | results

        finall_stats = {
            hash_: self._is_dangerous_result(res) for hash_, res in statuses.items()
        }
        logger.info(f'Checked {len(finall_stats)} files')

        session = session_factory()
        db_email = session.query(DBEmail).filter(DBEmail.id == email.db_id).first()
        for hash_, is_dangerous in finall_stats.items():
            db_attachment = Attachment(
                hash_=hash_, is_dangerous=is_dangerous, email=db_email
            )
            session.add(db_attachment)
        session.commit()
        session.close()
        logger.info('Attachments saved to DB')

        return any(finall_stats.values())
