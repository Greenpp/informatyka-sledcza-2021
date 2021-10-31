# %%
import logging

from email_proxy.sender.sender import EmailSender

logging.basicConfig(level=logging.DEBUG)

# %%
s = EmailSender()
# %%
s.load_emails()
# %%
s.send_emails()
# %%
