try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re


class SIPHeaderField(object):
    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def newForAttributes(cls, fieldName="", fieldValue=""):
        return cls.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

    @classmethod
    def newForFieldAttributes(cls, fieldName="", fieldValue=""):
        answer = cls()
        answer.fieldName = fieldName
        answer.fieldValue = fieldValue
        return answer

    @classmethod
    def canonicalFieldName(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def __init__(self):
        self._rawString = None
        self._fieldName = None
        self._fieldValue = None

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, aString):
        self._rawString = aString
        self.clearAttributes()

    @property
    def fieldName(self):
        if self._fieldName is None:
            self.parseAttributesFromRawString()
        return self._fieldName

    @fieldName.setter
    def fieldName(self, aString):
        self._fieldName = aString
        self.clearRawString()

    @property
    def fieldValue(self):
        if self._fieldValue is None:
            self.parseAttributesFromRawString()
        return self._fieldValue

    @fieldValue.setter
    def fieldValue(self, aString):
        self._fieldValue = aString
        self.clearRawString()

    # TODO: Answer a dict of parameter names and values encoded into the field value.
    # TODO: need to test
    # TODO: need to cache
    # TODO: possibly refactor this into a mixin.
    @property
    def parameterNamesAndValues(self):
        # RFC3261  7.3.1 Header Field Format
        # return dict(re.findall(';([^=]+)=([^;]+)', self.fieldValue))
        return dict(re.findall(';([^=;]+)=?([^;]+)?', self.fieldValue))

    def parameterNamed(self, aString):
        return self.parameterNamesAndValues.get(aString, None)

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        self._fieldName = None
        self._fieldValue = None

    def parseAttributesFromRawString(self):
        self._fieldName = ""
        self._fieldValue = ""
        match = self.__class__.regexForParsingFieldAndValue().match(self._rawString)
        if match:
            self._fieldName, self._fieldValue = match.group(1, 2)

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(str(self._fieldName))
        stringio.write(": ")
        stringio.write(str(self._fieldValue))
        self._rawString = stringio.getvalue()
        stringio.close()

    @classmethod
    def regexForMatchingFieldName(cls):
        return cls.regexToNeverMatch()

    @classmethod
    def regexForMatching(cls):
        return cls.regexForParsing()

    @classmethod
    def regexForParsing(cls):
        return cls.regexToNeverMatch()

    @classmethod
    def regexToNeverMatch(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    @classmethod
    def regexForParsingFieldAndValue(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def canMatchString(cls, aString):
        return cls.regexForMatching().match(aString) is not None

    @classmethod
    def canMatchFieldName(cls, aString):
        return cls.regexForMatchingFieldName().match(aString) is not None

    @property
    def isUnknown(self):
        return not self.isKnown

    @property
    def isKnown(self):
        return True

    @property
    def isValid(self):
        if not self.fieldName:  # fail if None or empty fieldName.
            return False
        if self.fieldValue is None:
            return False
        return True

    @property
    def isAccept(self):
        return False

    @property
    def isAcceptEncoding(self):
        return False

    @property
    def isAcceptLanguage(self):
        return False

    @property
    def isAllow(self):
        return False

    @property
    def isAuthorization(self):
        return False

    @property
    def isCSeq(self):
        return False

    @property
    def isCallID(self):
        return False

    @property
    def isCallInfo(self):
        return False

    @property
    def isContact(self):
        return False

    @property
    def isContentDisposition(self):
        return False

    @property
    def isContentType(self):
        return False

    @property
    def isContentLength(self):
        return False

    @property
    def isDate(self):
        return False

    @property
    def isExpires(self):
        return False

    @property
    def isFrom(self):
        return False

    @property
    def isMaxForwards(self):
        return False

    @property
    def isRecordRoute(self):
        return False

    @property
    def isRequire(self):
        return False

    @property
    def isRetryAfter(self):
        return False

    @property
    def isRoute(self):
        return False

    @property
    def isServer(self):
        return False

    @property
    def isSessionExpires(self):
        return False

    @property
    def isSupported(self):
        return False

    @property
    def isTimestamp(self):
        return False

    @property
    def isTo(self):
        return False

    @property
    def isUserAgent(self):
        return False

    @property
    def isVia(self):
        return False

    @property
    def isWWWAuthenticate(self):
        return False

    @property
    def isWarning(self):
        return False

