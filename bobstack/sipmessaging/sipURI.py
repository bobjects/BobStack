try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re

# TODO: We use regular expressions to parse this.  That will miss some edge cases, and will not
# correctly parse escaped strings or IPv6, I don't think.  We will either need to revisit our regexes, or use something
# like ANTLR to create a parser.  The RFC4475 and RFC5118 torture tests should inform that.


class SIPURI(object):
    regex_for_parsing_host_port = re.compile('([^:]*):?(.*)')
    regexForFindingParameterNamesAndValues = re.compile(';([^=;]+)=?([^;]+)?')
    regexForURI = re.compile('(([^:]*):([^@;]*)@?([^;]*)?)')

    @classmethod
    def new_parsed_from(cls, a_string):
        answer = cls()
        answer.raw_string = a_string
        return answer

    @classmethod
    def new_for_attributes(cls, host='', port=None, scheme='sip', user=None, parameter_names_and_value_strings=None):
        answer = cls()
        answer.host = host
        answer.port = port
        answer.scheme = scheme
        answer.user = user
        answer.parameter_names_and_value_strings = parameter_names_and_value_strings
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

        self.clear_raw_string()
        self.clear_attributes()

    @property
    def raw_string(self):
        if self._rawString is None:
            self.render_raw_string_from_attributes()
        return self._rawString

    @raw_string.setter
    def raw_string(self, a_string):
        self._rawString = a_string
        self.clear_attributes()

    @property
    def host(self):
        if self._attributesMustBeParsed:
            self.parse_attributes_from_raw_string()
        return self._host

    @host.setter
    def host(self, a_string):
        self._host = a_string
        self.clear_raw_string()

    @property
    def derived_port(self):
        if self.port is not None:
            return self.port
        else:
            if self.scheme == 'sips':
                return 5061
            else:
                return 5060

    @property
    def port(self):
        if self._attributesMustBeParsed:
            self.parse_attributes_from_raw_string()
        return self._port

    @port.setter
    def port(self, an_integer):
        self._port = an_integer
        self.clear_raw_string()

    @property
    def scheme(self):
        if self._attributesMustBeParsed:
            self.parse_attributes_from_raw_string()
        return self._scheme

    @scheme.setter
    def scheme(self, a_string):
        self._scheme = a_string
        self.clear_raw_string()

    @property
    def user(self):
        if self._attributesMustBeParsed:
            self.parse_attributes_from_raw_string()
        return self._user

    @user.setter
    def user(self, a_string):
        self._user = a_string
        self.clear_raw_string()

    @property
    def parameter_names_and_value_strings(self):
        if self._attributesMustBeParsed:
            self.parse_attributes_from_raw_string()
        if self._parameterNamesAndValueStrings is None:
            self._parameterNamesAndValueStrings = {}
        return self._parameterNamesAndValueStrings

    @parameter_names_and_value_strings.setter
    def parameter_names_and_value_strings(self, a_dictionary):
        self._parameterNamesAndValueStrings = a_dictionary
        self.clear_raw_string()

    # TODO: need to test.
    @property
    def parameter_names(self):
        return self.parameter_names_and_value_strings.keys()

    def parameter_named(self, key_string):
        return self.parameter_names_and_value_strings.get(key_string, None)

    def parameter_named_put(self, key_string, value_object):
        if not self.parameter_names_and_value_strings:
            self.parameter_names_and_value_strings = {}
        self.parameter_names_and_value_strings[key_string] = value_object
        self.clear_raw_string()

    def clear_raw_string(self):
        self._attributesMustBeParsed = False
        self._rawString = None

    def clear_attributes(self):
        self._host = None
        self._port = None
        self._scheme = None
        self._user = None
        self._parameterNamesAndValueStrings = None
        self._attributesMustBeParsed = True

    def parse_attributes_from_raw_string(self):
        self.clear_attributes()
        self._attributesMustBeParsed = False
        # TODO - put in exception handler for malformed SIPURI, after we do some testing.
        self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self._rawString))
        uri_match_groups = self.__class__.regexForURI.match(self._rawString).groups()
        # parsedAttributes['sip_uri'] = uri_match_groups[0]
        self._scheme = uri_match_groups[1]
        if uri_match_groups[3]:
            self._user = uri_match_groups[2]
            host_port = uri_match_groups[3]
        else:
            self._user = None
            host_port = uri_match_groups[2]
        host_port_match_groups = self.__class__.regex_for_parsing_host_port.match(host_port).groups()
        self._host = host_port_match_groups[0]
        if host_port_match_groups[1]:
            self._port = int(host_port_match_groups[1])

    def render_raw_string_from_attributes(self):
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
        if self.parameter_names_and_value_strings:
            for key, value in self.parameter_names_and_value_strings.iteritems():
                stringio.write(';')
                stringio.write(str(key))
                stringio.write('=')
                stringio.write(str(value))
        self._rawString = stringio.getvalue()
        stringio.close()
