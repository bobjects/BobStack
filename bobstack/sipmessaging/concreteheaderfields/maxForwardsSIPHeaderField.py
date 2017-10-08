try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import IntegerSIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


class MaxForwardsSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Max-Forwards'

    @property
    def is_max_forwards(self):
        return True

