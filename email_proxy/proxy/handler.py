class AnalyzingProxy:
    def handle_DATA(self, server, session, envelope) -> str:
        return '250 OK'
    
    def _send_to_receiver(self) -> None:
        # TODO pass to receiver
        pass
    
    def _send_to_quarantine(self) -> None:
        # TODO pass to quarantine
        pass

# NOTE build-in simple proxy handler
# class Proxy:
#     def __init__(self, remote_hostname, remote_port):
#         self._hostname = remote_hostname
#         self._port = remote_port

#     async def handle_DATA(self, server, session, envelope):
#         if isinstance(envelope.content, str):
#             content = envelope.original_content
#         else:
#             content = envelope.content
#         lines = content.splitlines(keepends=True)
#         # Look for the last header
#         _i = 0
#         ending = CRLF
#         for _i, line in enumerate(lines):  # pragma: nobranch
#             if NLCRE.match(line):
#                 ending = line
#                 break
#         peer = session.peer[0].encode('ascii')
#         lines.insert(_i, b'X-Peer: %s%s' % (peer, ending))
#         data = EMPTYBYTES.join(lines)
#         refused = self._deliver(envelope.mail_from, envelope.rcpt_tos, data)
#         # TBD: what to do with refused addresses?
#         log.info('we got some refusals: %s', refused)
#         return '250 OK'

#     def _deliver(self, mail_from, rcpt_tos, data):
#         refused = {}
#         try:
#             s = smtplib.SMTP()
#             s.connect(self._hostname, self._port)
#             try:
#                 refused = s.sendmail(mail_from, rcpt_tos, data)
#             finally:
#                 s.quit()
#         except smtplib.SMTPRecipientsRefused as e:
#             log.info('got SMTPRecipientsRefused')
#             refused = e.recipients
#         except (OSError, smtplib.SMTPException) as e:
#             log.exception('got %s', e.__class__)
#             # All recipients were refused.  If the exception had an associated
#             # error code, use it.  Otherwise, fake it with a non-triggering
#             # exception code.
#             errcode = getattr(e, 'smtp_code', -1)
#             errmsg = getattr(e, 'smtp_error', 'ignore')
#             for r in rcpt_tos:
#                 refused[r] = (errcode, errmsg)
#         return refused