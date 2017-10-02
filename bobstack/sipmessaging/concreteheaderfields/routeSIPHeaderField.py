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
class RouteSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-20.34

    regexForAngleBracketForm = re.compile('(.*)<(.*)>(.*)')
    regexForNonAngleBracketForm = re.compile('([^;]*)(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Route'

    # noinspection PyMethodOverriding
    @classmethod
    def new_for_attributes(cls, sip_uri=None):
        answer = cls()
        answer.sip_uri = sip_uri
        answer._isValid = (sip_uri is not None)
        return answer

    def __init__(self):
        self._isValid = None
        self._sipURI = None
        super(RouteSIPHeaderField, self).__init__()

    @property
    def is_valid(self):
        if not self._attributeHasBeenSet:
            self.parse_attributes_from_field_value_string()
        return self._isValid

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
        super(RouteSIPHeaderField, self).clear_attributes()
        self._sipURI = None
        self._isValid = None

    def parse_attributes_from_field_value_string(self):
        self._parameterNamesAndValueStrings = {}
        self._sipURI = None

        # noinspection PyBroadException
        try:
            match = self.__class__.regexForAngleBracketForm.match(self.field_value_string)
            if match:
                # URI uses angle brackets
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
    def is_route(self):
        return True

