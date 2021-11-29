from abc import ABC, abstractmethod

from ...email import Email


class Filter(ABC):
    @abstractmethod
    def is_spam_or_dangerous(self, email: Email) -> bool:
        """Checks if email is a spam message or if is dangerous

        Args:
            email (Email): Email object

        Returns:
            bool: If is a spam message or if is dangerous
        """
        pass
