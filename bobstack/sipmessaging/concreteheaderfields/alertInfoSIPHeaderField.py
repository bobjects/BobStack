from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class AlertInfoSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Alert-Info'

    @classmethod
    def new_for_attributes(cls, field_name="Alert-Info", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_alert_info(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def appearance(self):
        return self.parameter_named('appearance')

    @appearance.setter
    def appearance(self, a_string):
        self.parameter_named_put('appearance', a_string)

