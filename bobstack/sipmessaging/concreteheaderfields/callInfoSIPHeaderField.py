try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class CallInfoSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Call-Info'

    @classmethod
    def new_for_attributes(cls, field_name="Call-Info", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_call_info(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def m(self):
        return self.parameter_named('m')

    @m.setter
    def m(self, a_string):
        self.parameter_named_put('m', a_string)

    @property
    def purpose(self):
        return self.parameter_named('purpose')

    @purpose.setter
    def purpose(self, a_string):
        self.parameter_named_put('purpose', a_string)
