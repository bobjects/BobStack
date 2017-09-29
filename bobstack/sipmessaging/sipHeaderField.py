try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import inspect
from classproperty import classproperty

# TODO:  we need to formally test compact headers, beyond what is already being done in the sip torture test.
# TODO:  More to do, in other classes, to fully implement use_compact_headers.


class SIPHeaderField(object):
    regexForFindingParameterNamesAndValues = re.compile(";([^=;]+)=?([^;]+)?")
    regexForFindingValueUpToParameters = re.compile('([^;])')

    @classmethod
    def newParsedFrom(cls, a_string, use_compact_headers=False):
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.rawString = a_string
        return answer

    @classmethod
    def newForAttributes(cls, value='', parameterNamesAndValueStrings=None, use_compact_headers=False):
        # This will typically be overridden by classes that have interesting attributes.
        # return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.value = value
        if parameterNamesAndValueStrings:
            answer.parameterNamesAndValueStrings = parameterNamesAndValueStrings
        else:
            answer.parameterNamesAndValueStrings = {}
        return answer

    @classmethod
    def newForFieldNameAndValueString(cls, field_name="", field_value_string="", use_compact_headers=False):
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.field_name = field_name
        answer.field_value_string = field_value_string
        return answer

    @classmethod
    def newForValueString(cls, field_value_string, use_compact_headers=False):
        return cls.newForFieldNameAndValueString(cls.canonicalFieldName, field_value_string, use_compact_headers)

    @property
    def deepCopy(self):
        return self.__class__.newParsedFrom(self.rawString, use_compact_headers=self.use_compact_headers)

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return None

    def __init__(self):
        self._value = None
        self._attributeHasBeenSet = None
        self._rawStringHasBeenSet = None
        self._rawString = None
        self._parameterNamesAndValueStrings = None
        self._fieldName = None
        self._fieldNameAndValueStringHasBeenSet = None
        self._fieldValueString = None
        self._useCompactHeaders = False

        self.clearRawString()
        self.clearFieldNameAndValueString()
        self.clearAttributes()

    @property
    def rawString(self):
        if not self._rawStringHasBeenSet:
            self.renderRawStringFromFieldNameAndValueString()
        return self._rawString

    @rawString.setter
    def rawString(self, a_string):
        self._rawString = a_string
        self._rawStringHasBeenSet = True
        self.clearFieldNameAndValueString()
        self.clearAttributes()

    @property
    def use_compact_headers(self):
        return self._useCompactHeaders

    @use_compact_headers.setter
    def use_compact_headers(self, aBoolean):
        self._useCompactHeaders = aBoolean
        # noinspection PyUnusedLocal
        fieldValue = self.field_value_string  # render field values if not already rendered.
        self.clearRawString()

    @property
    def field_name(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.renderFieldNameAndValueStringFromAttributes()
            elif self._rawStringHasBeenSet:
                self.parseFieldNameAndValueStringFromRawString()
        return self._fieldName

    @field_name.setter
    def field_name(self, a_string):
        self._fieldName = a_string
        self._fieldNameAndValueStringHasBeenSet = True
        self.clearRawString()
        self.clearAttributes()

    @property
    def field_value_string(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.renderFieldNameAndValueStringFromAttributes()
            elif self._rawStringHasBeenSet:
                self.parseFieldNameAndValueStringFromRawString()
        return self._fieldValueString

    @field_value_string.setter
    def field_value_string(self, a_string):
        self._fieldValueString = a_string
        self._fieldNameAndValueStringHasBeenSet = True
        self.clearRawString()
        self.clearAttributes()

    @property
    def value(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    # TODO: Answer a dict of parameter names and values encoded into the field value.
    # TODO: need to test
    # TODO: need to cache
    # TODO: possibly refactor this into a mixin.
    @property
    def parameterNamesAndValueStrings(self):
        # RFC3261  7.3.1 Header Field Format
        # return dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self.field_value_string))
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._parameterNamesAndValueStrings

    @parameterNamesAndValueStrings.setter
    def parameterNamesAndValueStrings(self, aDictionary):
        self._parameterNamesAndValueStrings = aDictionary
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    def parameterNamed(self, a_string):
        return self.parameterNamesAndValueStrings.get(a_string, None)

    def parameterNamedPut(self, keyString, value):
        if value is None:
            self.parameterNamesAndValueStrings.pop(keyString, None)
        else:
            self.parameterNamesAndValueStrings[keyString] = value
        self.clearRawString()
        self.clearFieldNameAndValueString()

    def clearRawString(self):
        self._rawStringHasBeenSet = False
        self._rawString = None

    def clearAttributes(self):
        # override in subclasses that have interesting attributes.
        self._parameterNamesAndValueStrings = {}
        self._value = None
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
        if self.use_compact_headers:
            self._fieldName = self.canonicalCompactFieldName
        else:
            self._fieldName = self.canonicalFieldName
        if self.parameterNamesAndValueStrings:
            self._fieldValueString = str(self._value)
        else:
            stringio = StringIO()
            stringio.write(str(self._value))
            for key, value in self.parameterNamesAndValueStrings.iteritems():
                stringio.write(';')
                stringio.write(key)
                stringio.write('=')
                stringio.write(str(value))
            self._fieldValueString = stringio.getvalue()
            stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    def parseAttributesFromFieldValueString(self):
        self._value = self.field_value_string
        self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self.field_value_string))
        if self._parameterNamesAndValueStrings:
            self._value = self.__class__.regexForFindingValueUpToParameters.match(self.field_value_string).group(1)

    def renderRawStringFromFieldNameAndValueString(self):
        stringio = StringIO()
        stringio.write(str(self.field_name))
        stringio.write(": ")
        stringio.write(str(self.field_value_string))
        self._rawString = stringio.getvalue()
        stringio.close()
        self._rawStringHasBeenSet = True

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForMatchingFieldName(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            if cls.canonicalCompactFieldName:
                cls._regexForMatchingFieldName = re.compile('^(' + cls.canonicalFieldName + '|' + cls.canonicalCompactFieldName + ')$', re.I)
            else:
                cls._regexForMatchingFieldName = re.compile('^' + cls.canonicalFieldName + '$', re.I)
            return cls._regexForMatchingFieldName

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForMatching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            if cls.canonicalCompactFieldName:
                cls._regexForMatching = re.compile('^(' + cls.canonicalFieldName + '|' + cls.canonicalCompactFieldName + ')\s*:', re.I)
            else:
                cls._regexForMatching = re.compile('^' + cls.canonicalFieldName + '\s*:', re.I)
            return cls._regexForMatching

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForParsing(cls):
        return cls.regexToNeverMatch

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexToNeverMatch(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    # noinspection PyNestedDecorators,PyNestedDecorators
    @classproperty
    @classmethod
    def regexForParsingFieldAndValue(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def canMatchString(cls, a_string):
        return cls.regexForMatching.match(a_string) is not None

    @classmethod
    def canMatchFieldName(cls, a_string):
        return cls.regexForMatchingFieldName().match(a_string) is not None

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
        if not self.field_name:  # fail if None or empty field_name.
            return False
        if self.field_value_string is None:
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

    @property
    def isSubject(self):
        return False

    @property
    def isReferredBy(self):
        return False

    @property
    def isReferTo(self):
        return False

    @property
    def isAllowEvents(self):
        return False

    @property
    def isEvent(self):
        return False

    @property
    def isContentEncoding(self):
        return False

    @property
    def isRAck(self):
        return False

    @property
    def isPCharge(self):
        return False

    @property
    def isReplyTo(self):
        return False

    @property
    def isUnsupported(self):
        return False

    @property
    def isPAssertedIdentity(self):
        return False

    @property
    def isPPreferredIdentity(self):
        return False

    @property
    def isRemotePartyID(self):
        return False

    @property
    def isAlertInfo(self):
        return False

    @property
    def isHistoryInfo(self):
        return False

    @property
    def isPCalledPartyId(self):
        return False

    @property
    def isPRTPStat(self):
        return False

    @property
    def isPrivacy(self):
        return False

    @property
    def isProxyAuthenticate(self):
        return False

    @property
    def isProxyAuthorization(self):
        return False

    @property
    def isProxyRequire(self):
        return False

    @property
    def isReason(self):
        return False

    @property
    def isRecordSessionExpires(self):
        return False

    @property
    def isReplaces(self):
        return False

    @property
    def isSubscriptionState(self):
        return False

    @property
    def isMinExpires(self):
        return False

