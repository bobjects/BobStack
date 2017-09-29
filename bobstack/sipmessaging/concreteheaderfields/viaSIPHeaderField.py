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
    def host(self, a_string):
        self._host = a_string
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def port(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._port

    @port.setter
    def port(self, a_string):
        self._port = a_string
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def transport(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._transport

    @transport.setter
    def transport(self, a_string):
        self._transport = a_string
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    # TODO:  write tests, maybe cache.
    @property
    def asSIPURI(self):
        # Via contains the host, port, and transport portions in SIP URI form.  No user or scheme parts.
        # return SIPURI.newForAttributes(host=self.host, port=self.port, transport=self.transport)
        return SIPURI.newForAttributes(host=self.host, port=self.port)

    def generateBranch(self):
        self.branch = 'z9hG4bK-' + StrongRandomStringServer.instance.next32Bits + StrongRandomStringServer.instance.next32Bits + "-BobStack"

    def generateInvariantBranchForSIPHeader(self, a_sip_header):
        self.branch = 'z9hG4bK-' + a_sip_header.invariantBranchHash + "-BobStack"

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
            match = self.__class__.regexForViaSpecificValue.match(self.field_value_string)
            if not match:
                self._isValid = False
            else:
                #  self._isValid = (match.group(1) == 'SIP/2.0')
                sip_version = match.group(1)
                self._transport = match.group(2)
                host_port = match.group(3)
                host_port_match_groups = self.__class__.regexForParsingHostPort.match(host_port).groups()
                self._host = host_port_match_groups[0]
                if host_port_match_groups[1]:
                    self._port = int(host_port_match_groups[1])
                self._isValid = (sip_version == '2.0')
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

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def alias(self):
        return self.parameterNamed('alias')

    @alias.setter
    def alias(self, a_string):
        self.parameterNamedPut('alias', a_string)

    @property
    def branch(self):
        return self.parameterNamed('branch')

    @branch.setter
    def branch(self, a_string):
        self.parameterNamedPut('branch', a_string)

    @property
    def comp(self):
        return self.parameterNamed('comp')

    @comp.setter
    def comp(self, a_string):
        self.parameterNamedPut('comp', a_string)

    @property
    def keep(self):
        return self.parameterNamed('keep')

    @keep.setter
    def keep(self, a_string):
        self.parameterNamedPut('keep', a_string)

    @property
    def maddr(self):
        return self.parameterNamed('maddr')

    @maddr.setter
    def maddr(self, a_string):
        self.parameterNamedPut('maddr', a_string)

    @property
    def oc(self):
        return self.parameterNamed('oc')

    @oc.setter
    def oc(self, a_string):
        self.parameterNamedPut('oc', a_string)

    @property
    def oc_algo(self):
        return self.parameterNamed('oc-algo')

    @oc_algo.setter
    def oc_algo(self, a_string):
        self.parameterNamedPut('oc-algo', a_string)

    @property
    def oc_seq(self):
        return self.parameterNamed('oc-seq')

    @oc_seq.setter
    def oc_seq(self, a_string):
        self.parameterNamedPut('oc-seq', a_string)

    @property
    def oc_validity(self):
        return self.parameterNamed('oc-validity')

    @oc_validity.setter
    def oc_validity(self, a_string):
        self.parameterNamedPut('oc-validity', a_string)

    @property
    def received(self):
        return self.parameterNamed('received')

    @received.setter
    def received(self, a_string):
        self.parameterNamedPut('received', a_string)

    @property
    def rport(self):
        return self.parameterNamed('rport')

    @rport.setter
    def rport(self, a_string):
        self.parameterNamedPut('rport', a_string)

    @property
    def sigcomp_id(self):
        return self.parameterNamed('sigcomp-id')

    @sigcomp_id.setter
    def sigcomp_id(self, a_string):
        self.parameterNamedPut('sigcomp-id', a_string)

    @property
    def ttl(self):
        return self.parameterNamed('ttl')

    @ttl.setter
    def ttl(self, a_string):
        self.parameterNamedPut('ttl', a_string)
