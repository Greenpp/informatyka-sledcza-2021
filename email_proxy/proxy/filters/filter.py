from abc import ABC, abstractmethod


class Filter(ABC):
    @abstractmethod
    def is_spam_or_dangerous(self, email) -> bool:
        pass
