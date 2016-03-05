try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re


class SIPURI(object):
    @classmethod
    def newParsedFrom(cls, aString):
        answer = cls()
        answer.rawString = aString
        return answer

    @classmethod
    def newForAttributes(cls, host='', port=None, scheme='sip', user=None, parameterNamesAndValueStrings=None):
        answer = cls()
        cls.host = host
        cls.port = port
        cls.scheme = scheme
        cls.user = user
        cls.parameterNamesAndValueStrings = parameterNamesAndValueStrings
        return answer

    def __init__(self):
        self._rawString = None
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
        if self._rawStringNeedsParsing:
            self.parseAttributesFromRawString()
        return self._host

    @host.setter
    def host(self, aString):
        self._host = aString
        self.clearRawString()

    @property
    def port(self):
        if self._rawStringNeedsParsing:
            self.parseAttributesFromRawString()
        return self._port

    @port.setter
    def port(self, anInteger):
        self._port = anInteger
        self.clearRawString()

    @property
    def scheme(self):
        if self._rawStringNeedsParsing:
            self.parseAttributesFromRawString()
        return self._scheme

    @scheme.setter
    def scheme(self, aString):
        self._scheme = aString
        self.clearRawString()

    @property
    def user(self):
        if self._rawStringNeedsParsing:
            self.parseAttributesFromRawString()
        return self._user

    @user.setter
    def user(self, aString):
        self._user = aString
        self.clearRawString()

    @property
    def parameterNamesAndValueStrings(self):
        if self._rawStringNeedsParsing:
            self.parseAttributesFromRawString()
        return self._parameterNamesAndValueStrings

    @parameterNamesAndValueStrings.setter
    def parameterNamesAndValueStrings(self, aDictionary):
        self._parameterNamesAndValueStrings = aDictionary
        self.clearRawString()

    def parameterNamed(self, keyString):
        return self.parameterNamesAndValueStrings.get(keyString, None)

    def parameterNamedPut(self, keyString, valueObject):
        self.parameterNamesAndValueStrings[keyString] = valueObject

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        self._host = None
        self._port = None
        self._scheme=None
        self._user=None
        self._parameterNamesAndValueStrings=None
        self._rawStringNeedsParsing = True

    def parseAttributesFromRawString(self):
        #TODO
        pass

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        scheme = self._scheme
        if not scheme:
            scheme = 'sip'
        stringio.write(str(self._scheme))
        stringio.write(':')
        if self.user:
            stringio.write(self.user)
            stringio.write('@')
        stringio.write(str(self.host))
        if self.port is not None:
            stringio.write(':')
            stringio.write(str(self.port))
        for key, value in enumerate(self.parameterNamesAndValueStrings):
            stringio.write(';')
            stringio.write(str(key))
            stringio.write('=')
            stringio.write(str(value))
        self._rawString = stringio.getvalue()
        stringio.close()
