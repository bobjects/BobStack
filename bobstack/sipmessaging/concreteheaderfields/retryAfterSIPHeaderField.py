try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import IntegerSIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import IntegerSIPHeaderField
from sipmessaging import classproperty


class RetryAfterSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Retry-After'

    @property
    def isRetryAfter(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def duration(self):
        return self.parameterNamed('duration')

    @duration.setter
    def duration(self, aString):
        self.parameterNamedPut('duration', aString)

