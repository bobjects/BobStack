try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
# from bobstack.sipmessaging import StrongRandomStringServer
from sipmessaging import SIPHeaderField
from sipmessaging import SIPURI
from sipmessaging import classproperty
from sipmessaging import StrongRandomStringServer


class ViaSIPHeaderField(SIPHeaderField):
    # TODO
    regexForViaSpecificValue = re.compile('SIP\s*/\s*(\d.\d)\s*/\s*([^\s]+)\s+([^;]+)')
    regexForParsingHostPort = re.compile('([^:]*):?(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Via'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'v'

    @classmethod
    def newForAttributes(cls, host='', port=None, transport=None, branch=None):
        answer = cls()
        answer.host = host
        answer.port = port
        answer.transport = transport
        answer.branch = branch
        answer._isValid = True
        return answer

    def __init__(self):
        self._host = None
        self._port = None
        self._transport = None
        self._isValid = None
        super(ViaSIPHeaderField, self).__init__()

    # TODO: when we do warnings, warn of branch that does not start with "z9hG4bKy", i.e. a non-RFC3261 message.  Also, a full-blown error if SIP/2.0 is not exactly that.
    @property
    def isValid(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._isValid

    @property
    def host(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._host

    @host.setter
    def host(self, aString):
        self._host = aString
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def port(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._port

    @port.setter
    def port(self, aString):
        self._port = aString
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def transport(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._transport

    @transport.setter
    def transport(self, aString):
        self._transport = aString
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    # TODO:  write tests, maybe cache.
    @property
    def asSIPURI(self):
        # Via contains the host, port, and transport portions in SIP URI form.  No user or scheme parts.
        return SIPURI.newForAttributes(host=self.host, port=self.port, transport=self.transport)

    @property
    def branch(self):
        return self.parameterNamed('branch')

    @branch.setter
    def branch(self, aString):
        self.parameterNamedPut('branch', aString)

    def generateBranch(self):
        self.branch = 'z9hG4bK-' + StrongRandomStringServer.instance.next32Bits + StrongRandomStringServer.instance.next32Bits + "-BobStack"

    def generateInvariantBranchForSIPHeader(self, aSIPHeader):
        self.branch = 'z9hG4bK-' + aSIPHeader.invariantBranchHash + "-BobStack"

    def clearAttributes(self):
        super(ViaSIPHeaderField, self).clearAttributes()
        self._host = None
        self._port = None
        self._isValid = None

    def parseAttributesFromFieldValueString(self):
        self._host = None
        self._port = None
        self._transport = None
        self._parameterNamesAndValueStrings = {}
        # noinspection PyBroadException
        try:
            super(ViaSIPHeaderField, self).parseAttributesFromFieldValueString()
            match = self.__class__.regexForViaSpecificValue.match(self.fieldValueString)
            if not match:
                self._isValid = False
            else:
                #  self._isValid = (match.group(1) == 'SIP/2.0')
                sipVersion = match.group(1)
                self._transport = match.group(2)
                hostPort = match.group(3)
                hostPortMatchGroups = self.__class__.regexForParsingHostPort.match(hostPort).groups()
                self._host = hostPortMatchGroups[0]
                if hostPortMatchGroups[1]:
                    self._port = int(hostPortMatchGroups[1])
                self._isValid = (sipVersion == '2.0')
            self._attributeHasBeenSet = True
            self._isValid = self._isValid and bool(self.branch)
        except Exception:
            self._isValid = False

    def renderFieldNameAndValueStringFromAttributes(self):
        self._fieldName = self.canonicalFieldName
        stringio = StringIO()
        stringio.write('SIP/2.0/')
        stringio.write(str(self._transport))
        stringio.write(' ')
        stringio.write(str(self._host))
        if self._port:
            stringio.write(':' + str(self._port))
        for key, value in self._parameterNamesAndValueStrings.iteritems():
            stringio.write(';')
            stringio.write(key)
            stringio.write('=')
            stringio.write(str(value))
        self._fieldValueString = stringio.getvalue()
        stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    @property
    def isVia(self):
        return True

