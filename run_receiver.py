#!/usr/bin/env python
import logging

from email_proxy import ReceiverHandler, SMTPServer
from email_proxy.settings import TARGET_HOST, TARGET_PORT

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('mail.log').disabled = True

    server = SMTPServer(
        ReceiverHandler(),
        TARGET_HOST,
        TARGET_PORT,
    )
    server.run()
