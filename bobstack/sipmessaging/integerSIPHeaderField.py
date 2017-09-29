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
    def newForFieldNameAndValueString(cls, field_name="", field_value_string="0", use_compact_headers=False):
        return super(IntegerSIPHeaderField, cls).newForFieldNameAndValueString(field_name, field_value_string, use_compact_headers)

    @classmethod
    def newForIntegerValue(cls, an_integer):
        return cls.newForValueString(str(an_integer))

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
    def integerValue(self, an_integer):
        self.value = str(an_integer)

    @property
    def isValid(self):
        # Answer false if the value is not present.
        # noinspection PyUnusedLocal
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(IntegerSIPHeaderField, self).isValid and self._value is not None
