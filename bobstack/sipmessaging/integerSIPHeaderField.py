try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import inspect
from classproperty import classproperty
from sipHeaderField import SIPHeaderField


class IntegerSIPHeaderField(SIPHeaderField):
    # TODO: need to deal with parameters as first-class attributes.
    regexForParsingInteger = re.compile('\s*(\d*)')

    @classmethod
    def newForFieldNameAndValueString(cls, fieldName="", fieldValueString="0", useCompactHeaders=False):
        return super(IntegerSIPHeaderField, cls).newForFieldNameAndValueString(fieldName, fieldValueString, useCompactHeaders)

    @classmethod
    def newForIntegerValue(cls, anInteger):
        return cls.newForValueString(str(anInteger))

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return None

    @property
    def integerValue(self):
        try:
            return int(self.value)
        except ValueError:
            return 0

    @integerValue.setter
    def integerValue(self, anInteger):
        self.value = str(anInteger)

    @property
    def isValid(self):
        # Answer false if the value is not present.
        # noinspection PyUnusedLocal
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(IntegerSIPHeaderField, self).isValid and self._value is not None
