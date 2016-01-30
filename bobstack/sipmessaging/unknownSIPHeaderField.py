from sipHeaderField import SIPHeaderField

class UnknownSIPHeaderField(SIPHeaderField):
    @classmethod
    def regexToMatch(cls):
        if not cls._regexToMatch:
            cls._regexToMatch = re.compile('^NEVERMATCH')
        return cls._regexToMatch

