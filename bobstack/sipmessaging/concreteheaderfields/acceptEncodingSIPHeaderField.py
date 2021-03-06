from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class AcceptEncodingSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Accept-Encoding'

    @classmethod
    def new_for_attributes(cls, field_name="Accept-Encoding", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_accept_encoding(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def q(self):
        return self.parameter_named('q')

    @q.setter
    def q(self, a_string):
        self.parameter_named_put('q', a_string)

