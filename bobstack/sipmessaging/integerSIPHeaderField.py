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
    def new_for_field_name_and_value_string(cls, field_name="", field_value_string="0", use_compact_headers=False):
        return super(IntegerSIPHeaderField, cls).new_for_field_name_and_value_string(field_name, field_value_string, use_compact_headers)

    @classmethod
    def new_for_integer_value(cls, an_integer):
        return cls.new_for_value_string(str(an_integer))

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return None

    @property
    def integer_value(self):
        try:
            return int(self.value)
        except ValueError:
            return 0

    @integer_value.setter
    def integer_value(self, an_integer):
        self.value = str(an_integer)

    @property
    def is_valid(self):
        # Answer false if the value is not present.
        # noinspection PyUnusedLocal
        test = self.value  # Make sure the attributes are lazily initialized.
        return super(IntegerSIPHeaderField, self).is_valid and self._value is not None
