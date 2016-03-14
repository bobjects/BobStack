import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class NOTIFYSIPRequest(SIPRequest):
    @property
    def isNOTIFYRequest(self):
        return True

    @property
    def isKnown(self):
        return True
