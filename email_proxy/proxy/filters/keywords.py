from ...email import Email
from ...settings import TRIGGER_WORDS_FILE
from .filter import Filter


class KeywordsFilter(Filter):
    """Checks emails based on spam words"""

    file_path = TRIGGER_WORDS_FILE

    def is_spam_or_dangerous(self, email: Email) -> bool:
        """Checks if any trigger word is in email subject or message

        Args:
            email (Email): Email object

        Returns:
            bool: If a word was found
        """
        message = (
            email.msg.lower()
            .replace('.', '')
            .replace('!', '')
            .replace('?', '')
            .split(' ')
        )
        subject = (
            email.subject.lower()
            .replace('.', '')
            .replace('!', '')
            .replace('?', '')
            .split(' ')
        )
        words_list = self._read_from_file(self.file_path)

        result = any(map(lambda x: x in message or x in subject, words_list))

        return result

    def _read_from_file(self, path: str) -> list:
        "Reads a trigger word list from file"
        with open(path, 'r') as f:
            trigger_words = f.read().split(',')

        trigger_words = [word.lower() for word in trigger_words]

        return trigger_words
