try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import SIPURI
from ...sipmessaging import classproperty
from ...sipmessaging import StrongRandomStringServer


class ViaSIPHeaderField(SIPHeaderField):
    # TODO
    regexForViaSpecificValue = re.compile('SIP\s*/\s*(\d.\d)\s*/\s*([^\s]+)\s+([^;]+)')
    regex_for_parsing_host_port = re.compile('([^:]*):?(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Via'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'v'

    @classmethod
    def new_for_attributes(cls, host='', port=None, transport=None, branch=None):
        answer = cls()
        answer.host = host
        answer.port = port
        answer.transport = transport
        answer.branch = branch
        answer._is_valid = True
        return answer

    def __init__(self):
        self._host = None
        self._port = None
        self._transport = None
        self._is_valid = None
        super(ViaSIPHeaderField, self).__init__()

    # TODO: when we do warnings, warn of branch that does not start with "z9hG4bKy", i.e. a non-RFC3261 message.  Also, a full-blown error if SIP/2.0 is not exactly that.
    @property
    def is_valid(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._is_valid

    @property
    def host(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._host

    @host.setter
    def host(self, a_string):
        self._host = a_string
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    @property
    def port(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._port

    @port.setter
    def port(self, a_string):
        self._port = a_string
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    @property
    def transport(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._transport

    @transport.setter
    def transport(self, a_string):
        self._transport = a_string
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    # TODO:  write tests, maybe cache.
    @property
    def as_sip_uri(self):
        # Via contains the host, port, and transport portions in SIP URI form.  No user or scheme parts.
        # return SIPURI.new_for_attributes(host=self.host, port=self.port, transport=self.transport)
        return SIPURI.new_for_attributes(host=self.host, port=self.port)

    def generate_branch(self):
        self.branch = 'z9hG4bK-' + StrongRandomStringServer.instance.next_32_bits + StrongRandomStringServer.instance.next_32_bits + "-BobStack"

    def generate_invariant_branch_for_sip_header(self, a_sip_header):
        self.branch = 'z9hG4bK-' + a_sip_header.invariant_branch_hash + "-BobStack"

    def clear_attributes(self):
        super(ViaSIPHeaderField, self).clear_attributes()
        self._host = None
        self._port = None
        self._is_valid = None

    def parse_attributes_from_field_value_string(self):
        self._host = None
        self._port = None
        self._transport = None
        self._parameterNamesAndValueStrings = {}
        # noinspection PyBroadException
        try:
            super(ViaSIPHeaderField, self).parse_attributes_from_field_value_string()
            match = self.__class__.regexForViaSpecificValue.match(self.field_value_string)
            if not match:
                self._is_valid = False
            else:
                #  self._is_valid = (match.group(1) == 'SIP/2.0')
                sip_version = match.group(1)
                self._transport = match.group(2)
                host_port = match.group(3)
                host_port_match_groups = self.__class__.regex_for_parsing_host_port.match(host_port).groups()
                self._host = host_port_match_groups[0]
                if host_port_match_groups[1]:
                    self._port = int(host_port_match_groups[1])
                self._is_valid = (sip_version == '2.0')
            self._attributeHasBeenSet = True
            self._is_valid = self._is_valid and bool(self.branch)
        except Exception:
            self._is_valid = False

    def render_field_name_and_value_string_from_attributes(self):
        self._fieldName = self.canonical_field_name
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
    def is_via(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def alias(self):
        return self.parameter_named('alias')

    @alias.setter
    def alias(self, a_string):
        self.parameter_named_put('alias', a_string)

    @property
    def branch(self):
        return self.parameter_named('branch')

    @branch.setter
    def branch(self, a_string):
        self.parameter_named_put('branch', a_string)

    @property
    def comp(self):
        return self.parameter_named('comp')

    @comp.setter
    def comp(self, a_string):
        self.parameter_named_put('comp', a_string)

    @property
    def keep(self):
        return self.parameter_named('keep')

    @keep.setter
    def keep(self, a_string):
        self.parameter_named_put('keep', a_string)

    @property
    def maddr(self):
        return self.parameter_named('maddr')

    @maddr.setter
    def maddr(self, a_string):
        self.parameter_named_put('maddr', a_string)

    @property
    def oc(self):
        return self.parameter_named('oc')

    @oc.setter
    def oc(self, a_string):
        self.parameter_named_put('oc', a_string)

    @property
    def oc_algo(self):
        return self.parameter_named('oc-algo')

    @oc_algo.setter
    def oc_algo(self, a_string):
        self.parameter_named_put('oc-algo', a_string)

    @property
    def oc_seq(self):
        return self.parameter_named('oc-seq')

    @oc_seq.setter
    def oc_seq(self, a_string):
        self.parameter_named_put('oc-seq', a_string)

    @property
    def oc_validity(self):
        return self.parameter_named('oc-validity')

    @oc_validity.setter
    def oc_validity(self, a_string):
        self.parameter_named_put('oc-validity', a_string)

    @property
    def received(self):
        return self.parameter_named('received')

    @received.setter
    def received(self, a_string):
        self.parameter_named_put('received', a_string)

    @property
    def rport(self):
        return self.parameter_named('rport')

    @rport.setter
    def rport(self, a_string):
        self.parameter_named_put('rport', a_string)

    @property
    def sigcomp_id(self):
        return self.parameter_named('sigcomp-id')

    @sigcomp_id.setter
    def sigcomp_id(self, a_string):
        self.parameter_named_put('sigcomp-id', a_string)

    @property
    def ttl(self):
        return self.parameter_named('ttl')

    @ttl.setter
    def ttl(self, a_string):
        self.parameter_named_put('ttl', a_string)
