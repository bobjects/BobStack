import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPRequest


class BYESIPRequest(SIPRequest):
    @property
    def isBYERequest(self):
        return True

    @property
    def isKnown(self):
        return True