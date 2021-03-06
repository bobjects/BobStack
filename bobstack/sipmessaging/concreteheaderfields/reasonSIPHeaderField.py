try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class ReasonSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Reason'

    @classmethod
    def new_for_attributes(cls, field_name="Reason", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_reason(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def cause(self):
        return self.parameter_named('cause')

    @cause.setter
    def cause(self, a_string):
        self.parameter_named_put('cause', a_string)

    @property
    def text(self):
        return self.parameter_named('text')

    @text.setter
    def text(self, a_string):
        self.parameter_named_put('text', a_string)

