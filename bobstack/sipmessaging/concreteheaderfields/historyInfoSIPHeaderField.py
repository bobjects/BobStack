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


class HistoryInfoSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'History-Info'

    @classmethod
    def new_for_attributes(cls, field_name="History-Info", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_history_info(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def mp(self):
        return self.parameter_named('mp')

    @mp.setter
    def mp(self, a_string):
        self.parameter_named_put('mp', a_string)

    @property
    def np(self):
        return self.parameter_named('np')

    @np.setter
    def np(self, a_string):
        self.parameter_named_put('np', a_string)

    @property
    def rc(self):
        return self.parameter_named('rc')

    @rc.setter
    def rc(self, a_string):
        self.parameter_named_put('rc', a_string)
