import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class PRACKSIPRequest(SIPRequest):
    @property
    def isPRACKRequest(self):
        return True

    @property
    def isKnown(self):
        return True
