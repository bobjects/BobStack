import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class ACKSIPRequest(SIPRequest):
    @property
    def isACKRequest(self):
        return True

    @property
    def isKnown(self):
        return True
