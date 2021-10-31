import logging

from email_proxy import ReceiverHandler, SMTPServer
from email_proxy.settings import TARGET_HOST, TARGET_PORT

logging.basicConfig(level=logging.DEBUG)

server = SMTPServer(
    ReceiverHandler(),
    TARGET_HOST,
    TARGET_PORT,
)
server.run()
