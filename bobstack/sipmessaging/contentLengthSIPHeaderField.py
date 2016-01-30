import re
from sipHeaderField import SIPHeaderField


class ContentLengthSIPHeaderField(SIPHeaderField):
    @classmethod
    def regexToMatch(cls):
        try:
            return cls._regexToMatch
        except AttributeError:
            cls._regexToMatch = re.compile('^Content-Length\s*:\s*(\d*)', re.I)
            # cls._regexToMatch = re.compile('Content', re.I)
            return cls._regexToMatch

    @property
    def isValid(self):
        # TODO: Can we call the superclass property like this?  Hmm...
        # return SIPHeaderField.isValid(self) and self.value is not None
        return super(ContentLengthSIPHeaderField, self).isValid and self.value is not None

    @property
    def isContentLength(self):
        return True

    @property
    def value(self):
        try:
            return int(self.__class__.regexToMatch().match(self.rawString).group(1))
        except ValueError:
            return None
