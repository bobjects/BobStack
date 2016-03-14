import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class INFOSIPRequest(SIPRequest):
    @property
    def isINFORequest(self):
        return True

    @property
    def isKnown(self):
        return True
