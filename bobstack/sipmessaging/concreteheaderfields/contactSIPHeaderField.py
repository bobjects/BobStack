try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import SIPURI
# from bobstack.sipmessaging import classproperty
from sipmessaging import SIPHeaderField
from sipmessaging import SIPURI
from sipmessaging import classproperty


# TODO: may want to factor parsing from this, To, and Contact into a mixin.
class ContactSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-8.1.1.3

    regexForAngleBracketForm = re.compile('(.*)<(.*)>(.*)')
    regexForNonAngleBracketForm = re.compile('([^;]*)(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Contact'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'm'

    @classmethod
    def new_for_attributes(cls, display_name=None, sip_uri=None):
        answer = cls()
        answer.display_name = display_name
        answer.sip_uri = sip_uri
        answer._isValid = (sip_uri is not None)
        return answer

    def __init__(self):
        self._displayName = None
        self._isValid = None
        self._sipURI = None
        super(ContactSIPHeaderField, self).__init__()

    @property
    def is_valid(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._isValid

    @property
    def display_name(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._displayName

    @display_name.setter
    def display_name(self, a_string):
        self._displayName = a_string
        self._isValid = (self._sipURI is not None)
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clearFieldNameAndValueString()

    @property
    def sip_uri(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._sipURI

    @sip_uri.setter
    def sip_uri(self, a_sip_uri):
        self._sipURI = a_sip_uri
        self._isValid = (self._sipURI is not None)
        self._attributeHasBeenSet = True
        self.clear_raw_string()
        self.clearFieldNameAndValueString()

    def clear_attributes(self):
        super(ContactSIPHeaderField, self).clear_attributes()
        self._displayName = None
        self._sipURI = None
        self._isValid = None

    def parse_attributes_from_field_value_string(self):
        self._parameterNamesAndValueStrings = {}
        self._displayName = None
        self._sipURI = None

        # noinspection PyBroadException
        try:
            match = self.__class__.regexForAngleBracketForm.match(self.field_value_string)
            if match:
                # URI uses angle brackets
                self._displayName = match.group(1)
                uri_and_parameter_string = match.group(2)
                self._sipURI = SIPURI.new_parsed_from(uri_and_parameter_string)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sip_uri gets parsed within our exception handler.
                header_field_parameters_string = match.group(3)
            else:
                # same logic as above, but work on sample, not uri_and_parameter_string.  This will be factored in the real solution.
                uri_and_header_field_parameters_match_groups = self.__class__.regexForNonAngleBracketForm.match(self.field_value_string).groups()
                uri_string = uri_and_header_field_parameters_match_groups[0]
                self._sipURI = SIPURI.new_parsed_from(uri_string)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sip_uri gets parsed within our exception handler.
                header_field_parameters_string = uri_and_header_field_parameters_match_groups[1]
            self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(header_field_parameters_string))
            self._attributeHasBeenSet = True
        except Exception:
            self._isValid = False
        else:
            self._isValid = True

    def render_field_name_and_value_string_from_attributes(self):
        self._fieldName = self.canonical_field_name
        stringio = StringIO()
        if self._displayName:
            stringio.write('"' + self._displayName + '"')
        stringio.write('<')
        if self._sipURI:
            stringio.write(self._sipURI.raw_string)
        stringio.write('>')
        for key, value in self._parameterNamesAndValueStrings.iteritems():
            stringio.write(';')
            stringio.write(key)
            stringio.write('=')
            stringio.write(str(value))
        self._fieldValueString = stringio.getvalue()
        stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    @property
    def is_contact(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def expires(self):
        return self.parameter_named('expires')

    @expires.setter
    def expires(self, a_string):
        self.parameter_named_put('expires', a_string)

    @property
    def mp(self):
        return self.parameter_named('mp')

    @mp.setter
    def mp(self, a_string):
        self.parameter_named_put('mp', a_string)

    @property
    def np(self):
        return self.parameter_named('np')

    @np.setter
    def np(self, a_string):
        self.parameter_named_put('np', a_string)

    @property
    def pub_gruu(self):
        return self.parameter_named('pub-gruu')

    @pub_gruu.setter
    def pub_gruu(self, a_string):
        self.parameter_named_put('pub-gruu', a_string)

    @property
    def q(self):
        return self.parameter_named('q')

    @q.setter
    def q(self, a_string):
        self.parameter_named_put('q', a_string)

    @property
    def rc(self):
        return self.parameter_named('rc')

    @rc.setter
    def rc(self, a_string):
        self.parameter_named_put('rc', a_string)

    @property
    def reg_id(self):
        return self.parameter_named('reg-id')

    @reg_id.setter
    def reg_id(self, a_string):
        self.parameter_named_put('reg-id', a_string)

    @property
    def temp_gruu(self):
        return self.parameter_named('temp-gruu')

    @temp_gruu.setter
    def temp_gruu(self, a_string):
        self.parameter_named_put('temp-gruu', a_string)

    @property
    def temp_gruu_cookie(self):
        return self.parameter_named('temp-gruu-cookie')

    @temp_gruu_cookie.setter
    def temp_gruu_cookie(self, a_string):
        self.parameter_named_put('temp-gruu-cookie', a_string)



