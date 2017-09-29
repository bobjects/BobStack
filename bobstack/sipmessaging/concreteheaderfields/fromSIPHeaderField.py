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
# from bobstack.sipmessaging import StrongRandomStringServer
from sipmessaging import SIPHeaderField
from sipmessaging import SIPURI
from sipmessaging import classproperty
from sipmessaging import StrongRandomStringServer


# TODO: may want to factor parsing from this, To, and Contact into a mixin.
class FromSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-8.1.1.3

    regexForAngleBracketForm = re.compile('(.*)<(.*)>(.*)')
    regexForNonAngleBracketForm = re.compile('([^;]*)(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'From'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'f'

    @classmethod
    def newForAttributes(cls, tag=None, display_name=None, sip_uri=None):
        answer = cls()
        answer.tag = tag
        answer.display_name = display_name
        answer.sip_uri = sip_uri
        answer._isValid = (sip_uri is not None)
        return answer

    def __init__(self):
        self._displayName = None
        self._sipURI = None
        self._isValid = None
        super(FromSIPHeaderField, self).__init__()

    @property
    def isValid(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._isValid

    @property
    def display_name(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._displayName

    @display_name.setter
    def display_name(self, a_string):
        self._displayName = a_string
        self._isValid = (self._sipURI is not None)
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def sip_uri(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._sipURI

    @sip_uri.setter
    def sip_uri(self, a_sip_uri):
        self._sipURI = a_sip_uri
        self._isValid = (self._sipURI is not None)
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    def clearAttributes(self):
        super(FromSIPHeaderField, self).clearAttributes()
        self._displayName = None
        self._sipURI = None
        self._isValid = None

    def parseAttributesFromFieldValueString(self):
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
                self._sipURI = SIPURI.newParsedFrom(uri_and_parameter_string)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sip_uri gets parsed within our exception handler.
                header_field_parameters_string = match.group(3)
            else:
                # same logic as above, but work on sample, not uri_and_parameter_string.  This will be factored in the real solution.
                uri_and_header_field_parameters_match_groups = self.__class__.regexForNonAngleBracketForm.match(self.field_value_string).groups()
                uri_string = uri_and_header_field_parameters_match_groups[0]
                self._sipURI = SIPURI.newParsedFrom(uri_string)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sip_uri gets parsed within our exception handler.
                header_field_parameters_string = uri_and_header_field_parameters_match_groups[1]
            self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(header_field_parameters_string))
            self._attributeHasBeenSet = True
        except Exception:
            self._isValid = False
        else:
            self._isValid = True

    def renderFieldNameAndValueStringFromAttributes(self):
        self._fieldName = self.canonicalFieldName
        stringio = StringIO()
        if self._displayName:
            stringio.write('"' + self._displayName + '"')
        stringio.write('<')
        if self._sipURI:
            stringio.write(self._sipURI.rawString)
        stringio.write('>')
        for key, value in self._parameterNamesAndValueStrings.iteritems():
            stringio.write(';')
            stringio.write(key)
            stringio.write('=')
            stringio.write(str(value))
        self._fieldValueString = stringio.getvalue()
        stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    def generateTag(self):
        self.tag = StrongRandomStringServer.instance.next32Bits + "-BobStack"

    @property
    def isFrom(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def tag(self):
        return self.parameterNamed('tag')

    @tag.setter
    def tag(self, a_string):
        self.parameterNamedPut('tag', a_string)

