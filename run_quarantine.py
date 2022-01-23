#!/usr/bin/env python
import logging

from email_proxy import QuarantineHandler, SMTPServer
from email_proxy.settings import QUARANTINE_HOST, QUARANTINE_PORT

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('mail.log').disabled = True

    server = SMTPServer(
        QuarantineHandler(),
        QUARANTINE_HOST,
        QUARANTINE_PORT,
    )
    server.run()
