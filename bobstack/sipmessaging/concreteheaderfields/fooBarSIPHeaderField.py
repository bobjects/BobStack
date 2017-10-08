try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class FooBarSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Foo-Bar'

    @classmethod
    def new_for_attributes(cls, field_name="Foo-Bar", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_foo_bar(self):
        return True

