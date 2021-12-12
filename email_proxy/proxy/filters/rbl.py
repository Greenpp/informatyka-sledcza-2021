import itertools
import logging
from concurrent.futures import ThreadPoolExecutor

import requests

from ...email import Email
from ...settings import TINY_CP_RBLS
from .filter import Filter


class RBLFilter(Filter):
    """Checks emails using RBL"""

    rbl_list = TINY_CP_RBLS
    url_template = 'https://tinycp.com/ajax/rbl-check?ip={id}&rbl={rbl}'

    def is_spam_or_dangerous(self, email: Email) -> bool:
        with ThreadPoolExecutor() as e:
            results = list(
                e.map(
                    self._test_rbl,
                    itertools.repeat(email.sender),
                    self.rbl_list,
                )
            )

        return any(results)

    def _test_rbl(self, id: str, rbl: str) -> bool:
        """Tests given id (domain, ip, email address) against given RBL

        Args:
            id (str): Domain / ip / email address
            rbl (str): RBL name on tinycp

        Returns:
            bool: If id was found using this RBL
        """
        url = self.url_template.format(id=id, rbl=rbl)
        res = requests.get(url)

        if not res.ok:
            logging.warning(f'Failed to fetch RBL ({rbl})')
            return False

        return not res.text == 'false'
