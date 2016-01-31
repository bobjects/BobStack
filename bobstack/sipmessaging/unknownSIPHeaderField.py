import re
from sipHeaderField import SIPHeaderField


class UnknownSIPHeaderField(SIPHeaderField):
    @classmethod
    def regexForParsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^NEVERMATCH')
            return cls._regexForParsing

    @property
    def isKnown(self):
        return False
