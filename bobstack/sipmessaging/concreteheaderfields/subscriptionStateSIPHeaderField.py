try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import SIPHeaderField
from sipmessaging import classproperty


class SubscriptionStateSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Subscription-State'

    @classmethod
    def newForAttributes(cls, field_name="Subscription-State", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isSubscriptionState(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameterNamed('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, a_string):
        self.parameterNamedPut('adaptive-min-rate', a_string)

    @property
    def expires(self):
        return self.parameterNamed('expires')

    @expires.setter
    def expires(self, a_string):
        self.parameterNamedPut('expires', a_string)

    @property
    def max_rate(self):
        return self.parameterNamed('max-rate')

    @max_rate.setter
    def max_rate(self, a_string):
        self.parameterNamedPut('max-rate', a_string)

    @property
    def min_rate(self):
        return self.parameterNamed('min-rate')

    @min_rate.setter
    def min_rate(self, a_string):
        self.parameterNamedPut('min-rate', a_string)

    @property
    def reason(self):
        return self.parameterNamed('reason')

    @reason.setter
    def reason(self, a_string):
        self.parameterNamedPut('reason', a_string)

    @property
    def retry_after(self):
        return self.parameterNamed('retry-after')

    @retry_after.setter
    def retry_after(self, a_string):
        self.parameterNamedPut('retry-after', a_string)
