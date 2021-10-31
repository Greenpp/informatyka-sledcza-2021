# %%
import logging

from email_proxy import EmailProxy

logging.basicConfig(level=logging.DEBUG)

# %%
p = EmailProxy()

# %%
p.run()
# %%
