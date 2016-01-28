import re
from sipHeaderField import SIPHeaderField


class ContentLengthSIPHeaderField(SIPHeaderField):
    @classmethod
    def regexToMatch(cls):
        if not cls._regexToMatch:
            cls._regexToMatch = re._compile('^Content-Length[:\s]\s*(.*)')
        return cls._regexToMatch

    @property
    def isValid(self):
        # TODO: Can we call the superclass property like this?  Hmm...
        # return SIPHeaderField.isValid(self) and self.value is not None
        return super(ContentLengthSIPHeaderField, self).isValid and self.value is not None

    @property
    def value(self):
        try:
            return int(self.__class__.regexToMatch().match(self.rawString).group(1))
        except ValueError:
            return None
