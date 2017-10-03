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
    def canonical_field_name(cls):
        return 'Subscription-State'

    @classmethod
    def new_for_attributes(cls, field_name="Subscription-State", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_subscription_state(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameter_named('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, a_string):
        self.parameter_named_put('adaptive-min-rate', a_string)

    @property
    def expires(self):
        return self.parameter_named('expires')

    @expires.setter
    def expires(self, a_string):
        self.parameter_named_put('expires', a_string)

    @property
    def max_rate(self):
        return self.parameter_named('max-rate')

    @max_rate.setter
    def max_rate(self, a_string):
        self.parameter_named_put('max-rate', a_string)

    @property
    def min_rate(self):
        return self.parameter_named('min-rate')

    @min_rate.setter
    def min_rate(self, a_string):
        self.parameter_named_put('min-rate', a_string)

    @property
    def reason(self):
        return self.parameter_named('reason')

    @reason.setter
    def reason(self, a_string):
        self.parameter_named_put('reason', a_string)

    @property
    def retry_after(self):
        return self.parameter_named('retry-after')

    @retry_after.setter
    def retry_after(self, a_string):
        self.parameter_named_put('retry-after', a_string)
