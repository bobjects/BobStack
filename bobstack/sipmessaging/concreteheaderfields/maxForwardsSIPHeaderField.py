try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField


class MaxForwardsSIPHeaderField(IntegerSIPHeaderField):
    @classmethod
    def canonicalFieldName(cls):
        return 'Max-Forwards'

    @property
    def isMaxForwards(self):
        return True

