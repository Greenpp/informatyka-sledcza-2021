#!/usr/bin/env python
import logging

from email_proxy import EmailSender

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('mail.log').disabled = True

    sender = EmailSender()
    sender.load_emails()
    sender.send_emails()
