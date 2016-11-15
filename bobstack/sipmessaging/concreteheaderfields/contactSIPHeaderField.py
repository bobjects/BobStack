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
    def newForAttributes(cls, displayName=None, sipURI=None):
        answer = cls()
        answer.displayName = displayName
        answer.sipURI = sipURI
        answer._isValid = (sipURI is not None)
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
    def displayName(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._displayName

    @displayName.setter
    def displayName(self, aString):
        self._displayName = aString
        self._isValid = (self._sipURI is not None)
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def sipURI(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._sipURI

    @sipURI.setter
    def sipURI(self, aSIPURI):
        self._sipURI = aSIPURI
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
            match = self.__class__.regexForAngleBracketForm.match(self.fieldValueString)
            if match:
                # URI uses angle brackets
                self._displayName = match.group(1)
                uriAndParametersString = match.group(2)
                self._sipURI = SIPURI.newParsedFrom(uriAndParametersString)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sipURI gets parsed within our exception handler.
                headerFieldParametersString = match.group(3)
            else:
                # same logic as above, but work on sample, not uriAndParametersString.  This will be factored in the real solution.
                uriAndHeaderFieldParametersMatchGroups = self.__class__.regexForNonAngleBracketForm.match(self.fieldValueString).groups()
                uriString = uriAndHeaderFieldParametersMatchGroups[0]
                self._sipURI = SIPURI.newParsedFrom(uriString)
                # noinspection PyUnusedLocal
                foo = self._sipURI.user  # We do this to make sure the sipURI gets parsed within our exception handler.
                headerFieldParametersString = uriAndHeaderFieldParametersMatchGroups[1]
            self._parameterNamesAndValueStrings = dict(self.__class__.regexForFindingParameterNamesAndValues.findall(headerFieldParametersString))
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
    def expires(self, aString):
        self.parameterNamedPut('expires', aString)

    @property
    def mp(self):
        return self.parameterNamed('mp')

    @mp.setter
    def mp(self, aString):
        self.parameterNamedPut('mp', aString)

    @property
    def np(self):
        return self.parameterNamed('np')

    @np.setter
    def np(self, aString):
        self.parameterNamedPut('np', aString)

    @property
    def pub_gruu(self):
        return self.parameterNamed('pub-gruu')

    @pub_gruu.setter
    def pub_gruu(self, aString):
        self.parameterNamedPut('pub-gruu', aString)

    @property
    def q(self):
        return self.parameterNamed('q')

    @q.setter
    def q(self, aString):
        self.parameterNamedPut('q', aString)

    @property
    def rc(self):
        return self.parameterNamed('rc')

    @rc.setter
    def rc(self, aString):
        self.parameterNamedPut('rc', aString)

    @property
    def reg_id(self):
        return self.parameterNamed('reg-id')

    @reg_id.setter
    def reg_id(self, aString):
        self.parameterNamedPut('reg-id', aString)

    @property
    def temp_gruu(self):
        return self.parameterNamed('temp-gruu')

    @temp_gruu.setter
    def temp_gruu(self, aString):
        self.parameterNamedPut('temp-gruu', aString)

    @property
    def temp_gruu_cookie(self):
        return self.parameterNamed('temp-gruu-cookie')

    @temp_gruu_cookie.setter
    def temp_gruu_cookie(self, aString):
        self.parameterNamedPut('temp-gruu-cookie', aString)



