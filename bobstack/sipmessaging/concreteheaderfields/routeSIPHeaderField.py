try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPHeaderField
from bobstack.sipmessaging import SIPURI
from bobstack.sipmessaging import classproperty


# TODO: may want to factor parsing from this, To, and Contact into a mixin.
class RouteSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-20.34

    regexForAngleBracketForm = re.compile('(.*)<(.*)>(.*)')
    regexForNonAngleBracketForm = re.compile('([^;]*)(.*)')

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Route'

    # noinspection PyMethodOverriding
    @classmethod
    def newForAttributes(cls, sipURI=None):
        answer = cls()
        answer.sipURI = sipURI
        answer._isValid = (sipURI is not None)
        return answer

    def __init__(self):
        self._isValid = None
        self._sipURI = None
        super(RouteSIPHeaderField, self).__init__()

    @property
    def isValid(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._isValid

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
        super(RouteSIPHeaderField, self).clearAttributes()
        self._sipURI = None
        self._isValid = None

    def parseAttributesFromFieldValueString(self):
        self._parameterNamesAndValueStrings = {}
        self._sipURI = None

        # noinspection PyBroadException
        try:
            match = self.__class__.regexForAngleBracketForm.match(self.fieldValueString)
            if match:
                # URI uses angle brackets
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
    def isRoute(self):
        return True

