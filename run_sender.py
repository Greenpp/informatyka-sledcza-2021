import logging

from email_proxy import EmailSender

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    s = EmailSender()
    s.load_emails()
    s.send_emails()
