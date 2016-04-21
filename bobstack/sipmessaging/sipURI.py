try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re

# TODO: We use regular expressions to parse this.  That will miss some edge cases, and will not
# correctly parse escaped strings or IPv6, I don't think.  We will either need to revisit our regexes, or use something
# like ANTLR to create a parser.  The RFC4475 and RFC5118 torture tests should inform that.


class SIPURI(object):
    regexForParsingHostPort = re.compile('([^:]*):?(.*)')
    regexForFindingParameterNamesAndValues = re.compile(';([^=;]+)=?([^;]+)?')
    regexForURI = re.compile('(([^:]*):([^@;]*)@?([^;]*)?)')

    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def newForAttributes(cls, host='', port=None, scheme='sip', user=None, parameterNamesAndValueStrings=None):
        answer = cls()
        answer.host = host
        answer.port = port
        answer.scheme = scheme
        answer.user = user
        answer.parameterNamesAndValueStrings = parameterNamesAndValueStrings
        return answer

    def __init__(self):
        self._rawString = None
        self._user = None
        self._host = None
        self._port = None
        self._scheme = None
        self._user = None
        self._parameterNamesAndValueStrings = None
        self._attributesMustBeParsed = None

        self.clearRawString()
        self.clearAttributes()

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
    def host(self):
        if self._attributesMustBeParsed:
            self.parseAttributesFromRawString()
        return self._host

    @host.setter
    def host(self, aString):
        self._host = aString
        self.clearRawString()

    @property
    def port(self):
        if self._attributesMustBeParsed:
            self.parseAttributesFromRawString()
        return self._port

    @port.setter
    def port(self, anInteger):
        self._port = anInteger
        self.clearRawString()

    @property
    def scheme(self):
        if self._attributesMustBeParsed:
            self.parseAttributesFromRawString()
        return self._scheme

    @scheme.setter
    def scheme(self, aString):
        self._scheme = aString
        self.clearRawString()

    @property
    def user(self):
        if self._attributesMustBeParsed:
            self.parseAttributesFromRawString()
        return self._user

    @user.setter
    def user(self, aString):
        self._user = aString
        self.clearRawString()

    @property
    def parameterNamesAndValueStrings(self):
        if self._attributesMustBeParsed:
            self.parseAttributesFromRawString()
        if self._parameterNamesAndValueStrings is None:
            self._parameterNamesAndValueStrings = {}
        return self._parameterNamesAndValueStrings

    @parameterNamesAndValueStrings.setter
    def parameterNamesAndValueStrings(self, aDictionary):
        self._parameterNamesAndValueStrings = aDictionary
        self.clearRawString()

    # TODO: need to test.
    @property
    def parameterNames(self):
        return self.parameterNamesAndValueStrings.keys()

    def parameterNamed(self, keyString):
        return self.parameterNamesAndValueStrings.get(keyString, None)

    def parameterNamedPut(self, keyString, valueObject):
        if not self.parameterNamesAndValueStrings:
            self.parameterNamesAndValueStrings = {}
        self.parameterNamesAndValueStrings[keyString] = valueObject
        self.clearRawString()

    def clearRawString(self):
        self._attributesMustBeParsed = False
        self._rawString = None

    def clearAttributes(self):
        self._host = None
        self._port = None
        self._scheme = None
        self._user = None
        self._parameterNamesAndValueStrings = None
        self._attributesMustBeParsed = True

    def parseAttributesFromRawString(self):
        self.clearAttributes()
        self._attributesMustBeParsed = False
        # TODO - put in exception handler for malformed SIPURI, after we do some testing.
        self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self._rawString))
        uriMatchGroups = self.__class__.regexForURI.match(self._rawString).groups()
        # parsedAttributes['sipURI'] = uriMatchGroups[0]
        self._scheme = uriMatchGroups[1]
        if uriMatchGroups[3]:
            self._user = uriMatchGroups[2]
            hostPort = uriMatchGroups[3]
        else:
            self._user = None
            hostPort = uriMatchGroups[2]
        hostPortMatchGroups = self.__class__.regexForParsingHostPort.match(hostPort).groups()
        self._host = hostPortMatchGroups[0]
        if hostPortMatchGroups[1]:
            self._port = int(hostPortMatchGroups[1])

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        scheme = self.scheme
        if not scheme:
            scheme = 'sip'
        stringio.write(str(scheme))
        stringio.write(':')
        if self.user:
            stringio.write(self.user)
            stringio.write('@')
        stringio.write(str(self.host))
        if self.port is not None:
            stringio.write(':')
            stringio.write(str(self.port))
        if self.parameterNamesAndValueStrings:
            for key, value in self.parameterNamesAndValueStrings.iteritems():
                stringio.write(';')
                stringio.write(str(key))
                stringio.write('=')
                stringio.write(str(value))
        self._rawString = stringio.getvalue()
        stringio.close()
