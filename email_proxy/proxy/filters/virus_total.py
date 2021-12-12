from ...email import Email
from .filter import Filter


class VirusTotalFilter(Filter):
    def is_spam_or_dangerous(self, email: Email) -> bool:
        return False
