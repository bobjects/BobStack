try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import IntegerSIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import IntegerSIPHeaderField
from sipmessaging import classproperty


class MaxForwardsSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Max-Forwards'

    @property
    def isMaxForwards(self):
        return True

