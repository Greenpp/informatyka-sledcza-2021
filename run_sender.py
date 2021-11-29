import logging

from email_proxy import EmailSender

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sender = EmailSender()
    sender.load_emails()
    sender.send_emails()
