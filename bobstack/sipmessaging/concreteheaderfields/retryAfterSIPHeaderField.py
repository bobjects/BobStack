try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class RetryAfterSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Retry-After'

    @property
    def is_retry_after(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def duration(self):
        return self.parameter_named('duration')

    @duration.setter
    def duration(self, a_string):
        self.parameter_named_put('duration', a_string)

