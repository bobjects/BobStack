import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class REFERSIPRequest(SIPRequest):
    @property
    def isREFERRequest(self):
        return True

    @property
    def isKnown(self):
        return True
