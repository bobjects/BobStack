try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import inspect
from classproperty import classproperty


class SIPHeaderField(object):
    regexForFindingParameterNamesAndValues = re.compile(";([^=;]+)=?([^;]+)?")

    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def newForAttributes(cls, fieldName="", fieldValueString=""):
        # This will typically be overridden by classes that have interesting attributes.
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @classmethod
    def newForFieldNameAndValueString(cls, fieldName="", fieldValueString=""):
        answer = cls()
        answer.fieldName = fieldName
        answer.fieldValueString = fieldValueString
        return answer

    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def __init__(self):
        self.clearRawString()
        self.clearFieldNameAndValueString()
        self.clearAttributes()


    @property
    def rawString(self):
        if not self._rawStringHasBeenSet:
            self.renderRawStringFromFieldNameAndValueString()
        return self._rawString

    @rawString.setter
    def rawString(self, aString):
        self._rawString = aString
        self._rawStringHasBeenSet = True
        self.clearFieldNameAndValueString()
        self.clearAttributes()

    @property
    def fieldName(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.renderFieldNameAndValueStringFromAttributes()
            elif self._rawStringHasBeenSet:
                self.parseFieldNameAndValueStringFromRawString()
        return self._fieldName

    @fieldName.setter
    def fieldName(self, aString):
        self._fieldName = aString
        self._fieldNameAndValueStringHasBeenSet = True
        self.clearRawString()
        self.clearAttributes()

    @property
    def fieldValueString(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.renderFieldNameAndValueStringFromAttributes()
            elif self._rawStringHasBeenSet:
                self.parseFieldNameAndValueStringFromRawString()
        return self._fieldValueString

    @fieldValueString.setter
    def fieldValueString(self, aString):
        self._fieldValueString = aString
        self._fieldNameAndValueStringHasBeenSet = True
        self.clearRawString()
        self.clearAttributes()

    # TODO: Answer a dict of parameter names and values encoded into the field value.
    # TODO: need to test
    # TODO: need to cache
    # TODO: possibly refactor this into a mixin.
    @property
    def parameterNamesAndValueStrings(self):
        # RFC3261  7.3.1 Header Field Format
        # return dict(re.findall(';([^=;]+)=?([^;]+)?', self.fieldValueString))
        return dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self.fieldValueString))

    def parameterNamed(self, aString):
        return self.parameterNamesAndValueStrings.get(aString, None)

    def clearRawString(self):
        self._rawStringHasBeenSet = False
        self._rawString = None

    def clearAttributes(self):
        # override in subclasses that have interesting attributes.
        self._attributeHasBeenSet = False

    def clearFieldNameAndValueString(self):
        self._fieldName = None
        self._fieldValueString = None
        self._fieldNameAndValueStringHasBeenSet = False

    def parseFieldNameAndValueStringFromRawString(self):
        # self.clearAttributes()
        # self._attributeHasBeenSet = False
        self._fieldName = ""
        self._fieldValueString = ""
        match = self.__class__.regexForParsingFieldAndValue.match(self._rawString)
        if match:
            self._fieldName, self._fieldValueString = match.group(1, 2)
        self._fieldNameAndValueStringHasBeenSet = True

    def renderFieldNameAndValueStringFromAttributes(self):
        # override in subclasses that have interesting attributes.
        pass

    def parseAttributesFromFieldValueString(self):
        # override in subclasses that have interesting attributes.
        pass

    def renderRawStringFromFieldNameAndValueString(self):
        stringio = StringIO()
        stringio.write(str(self.fieldName))
        stringio.write(": ")
        stringio.write(str(self.fieldValueString))
        self._rawString = stringio.getvalue()
        stringio.close()
        self._rawStringHasBeenSet = True

    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            cls._regexForMatchingFieldName = re.compile('^' + cls.canonicalFieldName + '$', re.I)
            return cls._regexForMatchingFieldName
    '''
    @classproperty
    @classmethod
    def regexForMatching(cls):
        return cls.regexForParsing
    '''
    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            cls._regexForMatching = re.compile('^' + cls.canonicalFieldName + '\s*:', re.I)
            # cls._regexForMatching = re.compile('^To\s*:', re.I)
            return cls._regexForMatching


    @classproperty
    @classmethod
    def regexForParsing(cls):
        return cls.regexToNeverMatch

    @classproperty
    @classmethod
    def regexToNeverMatch(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    @classproperty
    @classmethod
    def regexForParsingFieldAndValue(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def canMatchString(cls, aString):
        return cls.regexForMatching.match(aString) is not None

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
    def isInvalid(self):
        return not self.isValid

    @property
    def isValid(self):
        if not self.fieldName:  # fail if None or empty fieldName.
            return False
        if self.fieldValueString is None:
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

