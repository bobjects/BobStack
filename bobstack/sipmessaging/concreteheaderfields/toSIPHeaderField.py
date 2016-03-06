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


class ToSIPHeaderField(SIPHeaderField):
    # https://tools.ietf.org/html/rfc3261#section-20.39

    # TODO: need to deal with parameters as first-class attributes.


    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'To'

    @classmethod
    def newForAttributes(cls, tag=None, displayName=None, sipURI=None):
        answer = cls()
        answer.tag = tag
        answer.displayName = displayName
        answer.sipURI = sipURI
        return answer

    @property
    def tag(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._tag

    @tag.setter
    def tag(self, aString):
        self._tag = aString
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    @property
    def displayName(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        return self._displayName

    @displayName.setter
    def displayName(self, aString):
        self._displayName = aString
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
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    def clearAttributes(self):
        super(ToSIPHeaderField, self).clearAttributes()
        self._tag = None
        self._displayName = None
        self._sipURI = None

    def parseAttributesFromFieldValueString(self):
        # TODO
        self._tag = None
        self._displayName = None
        self._sipURI = None
        super(ToSIPHeaderField, self).parseAttributesFromFieldValueString()
        # TODO: need to cache
        # TODO: need to parse out other header field parameters besides tag.

        match = re.match('(.*)<(.*)>(.*)', self.fieldValueString)
        headerFieldParametersString = ''
        if match:
            # URI uses angle brackets
            self._displayName = match.group(1)
            uriAndParametersString = match.group(2)
            self._sipURI = SIPURI.newParsedFrom(uriAndParametersString)
            headerFieldParametersString = match.group(3)
        else:
            # same logic as above, but work on sample, not uriAndParametersString.  This will be factored in the real solution.
            uriAndHeaderFieldParametersMatchGroups = re.match('([^;]*)(.*)', self.fieldValueString).groups()
            uriString = uriAndHeaderFieldParametersMatchGroups[1]
            self._sipURI = SIPURI.newParsedFrom(uriString)
            headerFieldParametersString = uriAndHeaderFieldParametersMatchGroups[2]
        headerFieldParameters = dict(re.findall(';([^=;]+)=?([^;]+)?', headerFieldParametersString))
        self._tag = headerFieldParameters.get('tag', None)
        self._attributeHasBeenSet = True

    def renderFieldNameAndValueStringFromAttributes(self):
        self._fieldName = self.canonicalFieldName
        # self._fieldValueString = str(self._value)
        stringio = StringIO()
        if self._displayName:
            stringio.write('"' + self._displayName + '"')
        stringio.write('<')
        if self._sipURI:
            stringio.write(self._sipURI.rawString)
        stringio.write('>')
        if self._tag:
            stringio.write(';tag=' + self._tag)
        # TODO:  need to do other header parameters.  Need to make them more first-class.
        self._fieldValueString = stringio.getvalue()
        stringio.close()
        self._fieldNameAndValueStringHasBeenSet = True

    # TODO
    @property
    def parameterNamesAndValueStrings(self):
        return {}

    '''
    @classmethod
    def newForAttributes(cls, fieldName="To", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
    '''
    '''
    # TODO: need to test
    # TODO: need to cache
    @property
    def tag(self):
        return self.parameterNamed("tag")

    # TODO
    def generateTag(self):
        pass
    '''

    @property
    def isTo(self):
        return True

