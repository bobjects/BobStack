try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class ContentDispositionSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Content-Disposition'

    @classmethod
    def new_for_attributes(cls, field_name="Content-Disposition", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_content_disposition(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def handling(self):
        return self.parameter_named('handling')

    @handling.setter
    def handling(self, a_string):
        self.parameter_named_put('handling', a_string)

