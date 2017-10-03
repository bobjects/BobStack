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
    def new_parsed_from(cls, a_string, use_compact_headers=False):
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.raw_string = a_string
        return answer

    @classmethod
    def new_for_attributes(cls, value='', parameter_names_and_value_strings=None, use_compact_headers=False):
        # This will typically be overridden by classes that have interesting attributes.
        # return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.value = value
        if parameter_names_and_value_strings:
            answer.parameter_names_and_value_strings = parameter_names_and_value_strings
        else:
            answer.parameter_names_and_value_strings = {}
        return answer

    @classmethod
    def new_for_field_name_and_value_string(cls, field_name="", field_value_string="", use_compact_headers=False):
        answer = cls()
        answer.use_compact_headers = use_compact_headers
        answer.field_name = field_name
        answer.field_value_string = field_value_string
        return answer

    @classmethod
    def new_for_value_string(cls, field_value_string, use_compact_headers=False):
        return cls.new_for_field_name_and_value_string(cls.canonical_field_name, field_value_string, use_compact_headers)

    @property
    def deep_copy(self):
        return self.__class__.new_parsed_from(self.raw_string, use_compact_headers=self.use_compact_headers)

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
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

        self.clear_raw_string()
        self.clear_field_name_and_value_string()
        self.clear_attributes()

    @property
    def raw_string(self):
        if not self._rawStringHasBeenSet:
            self.render_raw_string_from_field_name_and_value_string()
        return self._rawString

    @raw_string.setter
    def raw_string(self, a_string):
        self._rawString = a_string
        self._rawStringHasBeenSet = True
        self.clear_field_name_and_value_string()
        self.clear_attributes()

    @property
    def use_compact_headers(self):
        return self._useCompactHeaders

    @use_compact_headers.setter
    def use_compact_headers(self, a_boolean):
        self._useCompactHeaders = a_boolean
        # noinspection PyUnusedLocal
        field_value = self.field_value_string  # render field values if not already rendered.
        self.clear_raw_string()

    @property
    def field_name(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.render_field_name_and_value_string_from_attributes()
            elif self._rawStringHasBeenSet:
                self.parse_field_name_and_value_string_from_raw_string()
        return self._fieldName

    @field_name.setter
    def field_name(self, a_string):
        self._fieldName = a_string
        self._fieldNameAndValueStringHasBeenSet = True
        self.clear_raw_string()
        self.clear_attributes()

    @property
    def field_value_string(self):
        if not self._fieldNameAndValueStringHasBeenSet:
            if self._attributeHasBeenSet:
                self.render_field_name_and_value_string_from_attributes()
            elif self._rawStringHasBeenSet:
                self.parse_field_name_and_value_string_from_raw_string()
        return self._fieldValueString

    @field_value_string.setter
    def field_value_string(self, a_string):
        self._fieldValueString = a_string
        self._fieldNameAndValueStringHasBeenSet = True
        self.clear_raw_string()
        self.clear_attributes()

    @property
    def value(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    # TODO: Answer a dict of parameter names and values encoded into the field value.
    # TODO: need to test
    # TODO: need to cache
    # TODO: possibly refactor this into a mixin.
    @property
    def parameter_names_and_value_strings(self):
        # RFC3261  7.3.1 Header Field Format
        # return dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self.field_value_string))
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._parameterNamesAndValueStrings

    @parameter_names_and_value_strings.setter
    def parameter_names_and_value_strings(self, a_dictionary):
        self._parameterNamesAndValueStrings = a_dictionary
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    def parameter_named(self, a_string):
        return self.parameter_names_and_value_strings.get(a_string, None)

    def parameter_named_put(self, key_string, value):
        if value is None:
            self.parameter_names_and_value_strings.pop(key_string, None)
        else:
            self.parameter_names_and_value_strings[key_string] = value
        self.clear_raw_string()
        self.clear_field_name_and_value_string()

    def clear_raw_string(self):
        self._rawStringHasBeenSet = False
        self._rawString = None

    def clear_attributes(self):
        # override in subclasses that have interesting attributes.
        self._parameterNamesAndValueStrings = {}
        self._value = None
        self._attributeHasBeenSet = False

    def clear_field_name_and_value_string(self):
        self._fieldName = None
        self._fieldValueString = None
        self._fieldNameAndValueStringHasBeenSet = False

    def parse_field_name_and_value_string_from_raw_string(self):
        # self.clear_attributes()
        # self._attributeHasBeenSet = False
        self._fieldName = ""
        self._fieldValueString = ""
        match = self.__class__.regex_for_parsing_field_and_value.match(self._rawString)
        if match:
            self._fieldName, self._fieldValueString = match.group(1, 2)
        self._fieldNameAndValueStringHasBeenSet = True

    def render_field_name_and_value_string_from_attributes(self):
        if self.use_compact_headers:
            self._fieldName = self.canonical_compact_field_name
        else:
            self._fieldName = self.canonical_field_name
        if self.parameter_names_and_value_strings:
            self._fieldValueString = str(self._value)
        else:
            stringio = StringIO()
            stringio.write(str(self._value))
            for key, value in self.parameter_names_and_value_strings.iteritems():
                stringio.write(';')
                stringio.write(key)
                stringio.write('=')
                stringio.write(str(value))
            self._fieldValueString = stringio.getvalue()
            stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    def parse_attributes_from_field_value_string(self):
        self._value = self.field_value_string
        self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(self.field_value_string))
        if self._parameterNamesAndValueStrings:
            self._value = self.__class__.regexForFindingValueUpToParameters.match(self.field_value_string).group(1)

    def render_raw_string_from_field_name_and_value_string(self):
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
    def regex_for_matching_field_name(cls):
        try:
            return cls._regexForMatchingFieldName
        except AttributeError:
            if cls.canonical_compact_field_name:
                cls._regexForMatchingFieldName = re.compile('^(' + cls.canonical_field_name + '|' + cls.canonical_compact_field_name + ')$', re.I)
            else:
                cls._regexForMatchingFieldName = re.compile('^' + cls.canonical_field_name + '$', re.I)
            return cls._regexForMatchingFieldName

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regex_for_matching(cls):
        try:
            return cls._regexForMatching
        except AttributeError:
            if cls.canonical_compact_field_name:
                cls._regexForMatching = re.compile('^(' + cls.canonical_field_name + '|' + cls.canonical_compact_field_name + ')\s*:', re.I)
            else:
                cls._regexForMatching = re.compile('^' + cls.canonical_field_name + '\s*:', re.I)
            return cls._regexForMatching

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regex_for_parsing(cls):
        return cls.regex_to_never_match

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regex_to_never_match(cls):
        try:
            return cls._regexToNeverMatch
        except AttributeError:
            cls._regexToNeverMatch = re.compile('^NEVERMATCH')
            return cls._regexToNeverMatch

    # noinspection PyNestedDecorators,PyNestedDecorators
    @classproperty
    @classmethod
    def regex_for_parsing_field_and_value(cls):
        try:
            return cls._regexForParsingFieldAndValue
        except AttributeError:
            cls._regexForParsingFieldAndValue = re.compile('^([^\s:]+)\s*:\s*(.*)$')
            return cls._regexForParsingFieldAndValue

    @classmethod
    def can_match_string(cls, a_string):
        return cls.regex_for_matching.match(a_string) is not None

    @classmethod
    def can_match_field_name(cls, a_string):
        return cls.regex_for_matching_field_name().match(a_string) is not None

    @property
    def is_unknown(self):
        return not self.is_known

    @property
    def is_known(self):
        return True

    @property
    def is_invalid(self):
        return not self.is_valid

    @property
    def is_valid(self):
        if not self.field_name:  # fail if None or empty field_name.
            return False
        if self.field_value_string is None:
            return False
        return True

    @property
    def is_accept(self):
        return False

    @property
    def is_accept_encoding(self):
        return False

    @property
    def is_accept_language(self):
        return False

    @property
    def is_allow(self):
        return False

    @property
    def is_authorization(self):
        return False

    @property
    def is_cseq(self):
        return False

    @property
    def is_call_id(self):
        return False

    @property
    def is_call_info(self):
        return False

    @property
    def is_contact(self):
        return False

    @property
    def is_content_disposition(self):
        return False

    @property
    def is_content_type(self):
        return False

    @property
    def is_content_length(self):
        return False

    @property
    def is_date(self):
        return False

    @property
    def is_expires(self):
        return False

    @property
    def is_from(self):
        return False

    @property
    def is_max_forwards(self):
        return False

    @property
    def is_record_route(self):
        return False

    @property
    def is_require(self):
        return False

    @property
    def is_retry_after(self):
        return False

    @property
    def is_route(self):
        return False

    @property
    def is_server(self):
        return False

    @property
    def is_session_expires(self):
        return False

    @property
    def is_supported(self):
        return False

    @property
    def is_timestamp(self):
        return False

    @property
    def is_to(self):
        return False

    @property
    def is_user_agent(self):
        return False

    @property
    def is_via(self):
        return False

    @property
    def is_www_authenticate(self):
        return False

    @property
    def is_warning(self):
        return False

    @property
    def is_subject(self):
        return False

    @property
    def is_referred_by(self):
        return False

    @property
    def is_refer_to(self):
        return False

    @property
    def is_allow_events(self):
        return False

    @property
    def is_event(self):
        return False

    @property
    def is_content_encoding(self):
        return False

    @property
    def is_rack(self):
        return False

    @property
    def is_p_charge(self):
        return False

    @property
    def is_reply_to(self):
        return False

    @property
    def is_unsupported(self):
        return False

    @property
    def is_p_asserted_identity(self):
        return False

    @property
    def is_p_preferred_identity(self):
        return False

    @property
    def is_remote_party_id(self):
        return False

    @property
    def is_alert_info(self):
        return False

    @property
    def is_history_info(self):
        return False

    @property
    def is_p_called_party_id(self):
        return False

    @property
    def is_p_rtp_stat(self):
        return False

    @property
    def is_privacy(self):
        return False

    @property
    def is_proxy_authenticate(self):
        return False

    @property
    def is_proxy_authorization(self):
        return False

    @property
    def is_proxy_require(self):
        return False

    @property
    def is_reason(self):
        return False

    @property
    def is_record_session_expires(self):
        return False

    @property
    def is_replaces(self):
        return False

    @property
    def is_subscription_state(self):
        return False

    @property
    def is_min_expires(self):
        return False

