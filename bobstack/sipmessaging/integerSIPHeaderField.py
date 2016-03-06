try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
# sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
from classproperty import classproperty
from sipHeaderField import SIPHeaderField

class IntegerSIPHeaderField(SIPHeaderField):
    # TODO: need to deal with parameters as first-class attributes.
    regexForParsingInteger = re.compile('\s*(\d*)')

    @classmethod
    def newForAttributes(cls, value=0):
        answer = cls()
        answer.value = value
        return answer

    @classmethod
    def newForFieldNameAndValueString(cls, fieldName="", fieldValueString="0"):
        return super(IntegerSIPHeaderField,cls).newForFieldNameAndValueString(fieldName, fieldValueString)

    @property
    def value(self):
        if not self._attributeHasBeenSet:
            self.parseAttributesFromFieldValueString()
        if self._value is None:
            return 0
        return self._value

    @value.setter
    def value(self, anInteger):
        self._value = anInteger
        self._attributeHasBeenSet = True
        self.clearRawString()
        self.clearFieldNameAndValueString()

    def clearAttributes(self):
        super(IntegerSIPHeaderField, self).clearAttributes()
        self._value = None

    def parseAttributesFromFieldValueString(self):
        super(IntegerSIPHeaderField, self).parseAttributesFromFieldValueString()
        self._value = None
        match = self.__class__.regexForParsingInteger.match(self.fieldValueString)
        if match:
            matchGroup = match.group(1)
            if matchGroup:
                self._value = int(matchGroup)
            else:
                # Will get here if the header field is present, but there is no value.
                self._value = None
        self._attributeHasBeenSet = True

    def renderFieldNameAndValueStringFromAttributes(self):
        self._fieldName = self.canonicalFieldName
        self._fieldValueString = str(self._value)
        self._fieldNameAndValueStringHasBeenSet = True

    @property
    def isValid(self):
        # Answer false if the value is not present.
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(IntegerSIPHeaderField, self).isValid and self._value is not None
