import logging

from email_proxy import AnalyzingProxyHandler, SMTPServer
from email_proxy.settings import PROXY_HOST, PROXY_PORT

logging.basicConfig(level=logging.DEBUG)

server = SMTPServer(
    AnalyzingProxyHandler(),
    PROXY_HOST,
    PROXY_PORT,
)
server.run()
