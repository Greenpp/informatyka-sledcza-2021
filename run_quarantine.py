import logging

from email_proxy import QuarantineHandler, SMTPServer
from email_proxy.settings import QUARANTINE_HOST, QUARANTINE_PORT

logging.basicConfig(level=logging.DEBUG)

server = SMTPServer(
    QuarantineHandler(),
    QUARANTINE_HOST,
    QUARANTINE_PORT,
)
server.run()
