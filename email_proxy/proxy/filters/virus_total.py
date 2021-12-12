import hashlib
import io
import logging
import time
from typing import Optional

import vt
from dotenv import dotenv_values

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

    def _get_existing_scan_result(self, file_content: bytes) -> Optional[bool]:
        f_hash = hashlib.sha256(file_content).hexdigest()

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

    def _is_dangerous_result(self, result: dict) -> bool:
        return result['malicious'] or result['suspicious']

    def _join_results(self, ids: list[str]) -> list[dict]:
        id_status = {id_: False for id_ in ids}

        results = []
        for _ in range(VT_JOIN_RETRIES):
            for id_ in id_status.keys():
                if not id_status[id_]:
                    stat_obj = self.vt_client.get_object(f'/analyses/{id_}')
                    if stat_obj.status == 'completed':
                        results.append(stat_obj.stats)
                        id_status[id_] = True
            if not all(id_status.values()):
                time.sleep(VT_JOIN_DELAY)

        return results

    def is_spam_or_dangerous(self, email: Email) -> bool:
        results = []
        enqueued = []
        for f_name, f_content in email.attachments:
            logger.info(f'Checking file {f_name}')
            existing_status = self._get_existing_scan_result(f_content)
            if existing_status is not None:
                logger.info(f'File {f_name} result found')
                results.append(existing_status)
            else:
                logger.info(f'File {f_name} result not found, scanning')
                try:
                    scan_id = self._enqueue_file_scan(f_content)
                    enqueued.append(scan_id)
                except Exception as e:
                    logger.warning(f'Failed to scan file {f_name} | {e=}')

        logger.info('Joining results')
        scan_results = self._join_results(enqueued)
        statuses = scan_results + results

        finall_stats = [self._is_dangerous_result(r) for r in statuses]

        return any(finall_stats)
