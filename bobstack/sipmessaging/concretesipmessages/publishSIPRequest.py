import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class PUBLISHSIPRequest(SIPRequest):
    @property
    def isPUBLISHRequest(self):
        return True

    @property
    def isKnown(self):
        return True
