import re
from sipHeaderField import SIPHeaderField


class UnknownSIPHeaderField(SIPHeaderField):
    @classmethod
    def regexToMatch(cls):
        try:
            return cls._regexToMatch
        except AttributeError:
            cls._regexToMatch = re.compile('^NEVERMATCH')
            return cls._regexToMatch

    @property
    def isKnown(self):
        return False
