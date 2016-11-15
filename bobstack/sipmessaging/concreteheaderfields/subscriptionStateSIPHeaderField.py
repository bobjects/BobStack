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
    def newForAttributes(cls, fieldName="Subscription-State", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isSubscriptionState(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameterNamed('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, aString):
        self.parameterNamedPut('adaptive-min-rate', aString)

    @property
    def expires(self):
        return self.parameterNamed('expires')

    @expires.setter
    def expires(self, aString):
        self.parameterNamedPut('expires', aString)

    @property
    def max_rate(self):
        return self.parameterNamed('max-rate')

    @max_rate.setter
    def max_rate(self, aString):
        self.parameterNamedPut('max-rate', aString)

    @property
    def min_rate(self):
        return self.parameterNamed('min-rate')

    @min_rate.setter
    def min_rate(self, aString):
        self.parameterNamedPut('min-rate', aString)

    @property
    def reason(self):
        return self.parameterNamed('reason')

    @reason.setter
    def reason(self, aString):
        self.parameterNamedPut('reason', aString)

    @property
    def retry_after(self):
        return self.parameterNamed('retry-after')

    @retry_after.setter
    def retry_after(self, aString):
        self.parameterNamedPut('retry-after', aString)
