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
    def canonicalFieldName(cls):
        return 'Contact'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'm'

    @classmethod
    def newForAttributes(cls, display_name=None, sip_uri=None):
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
        super(ContactSIPHeaderField, self).clearAttributes()
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

    @property
    def isContact(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def expires(self):
        return self.parameterNamed('expires')

    @expires.setter
    def expires(self, a_string):
        self.parameterNamedPut('expires', a_string)

    @property
    def mp(self):
        return self.parameterNamed('mp')

    @mp.setter
    def mp(self, a_string):
        self.parameterNamedPut('mp', a_string)

    @property
    def np(self):
        return self.parameterNamed('np')

    @np.setter
    def np(self, a_string):
        self.parameterNamedPut('np', a_string)

    @property
    def pub_gruu(self):
        return self.parameterNamed('pub-gruu')

    @pub_gruu.setter
    def pub_gruu(self, a_string):
        self.parameterNamedPut('pub-gruu', a_string)

    @property
    def q(self):
        return self.parameterNamed('q')

    @q.setter
    def q(self, a_string):
        self.parameterNamedPut('q', a_string)

    @property
    def rc(self):
        return self.parameterNamed('rc')

    @rc.setter
    def rc(self, a_string):
        self.parameterNamedPut('rc', a_string)

    @property
    def reg_id(self):
        return self.parameterNamed('reg-id')

    @reg_id.setter
    def reg_id(self, a_string):
        self.parameterNamedPut('reg-id', a_string)

    @property
    def temp_gruu(self):
        return self.parameterNamed('temp-gruu')

    @temp_gruu.setter
    def temp_gruu(self, a_string):
        self.parameterNamedPut('temp-gruu', a_string)

    @property
    def temp_gruu_cookie(self):
        return self.parameterNamed('temp-gruu-cookie')

    @temp_gruu_cookie.setter
    def temp_gruu_cookie(self, a_string):
        self.parameterNamedPut('temp-gruu-cookie', a_string)



