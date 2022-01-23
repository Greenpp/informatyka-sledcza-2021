#!/usr/bin/env python
import logging

import nest_asyncio

from email_proxy import AnalyzingProxyHandler, SMTPServer
from email_proxy.settings import PROXY_HOST, PROXY_PORT

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('mail.log').disabled = True

    nest_asyncio.apply()
    server = SMTPServer(
        AnalyzingProxyHandler(),
        PROXY_HOST,
        PROXY_PORT,
    )
    server.run()
