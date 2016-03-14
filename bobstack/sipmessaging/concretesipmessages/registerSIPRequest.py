import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class REGISTERSIPRequest(SIPRequest):
    @property
    def isREGISTERRequest(self):
        return True

    @property
    def isKnown(self):
        return True
