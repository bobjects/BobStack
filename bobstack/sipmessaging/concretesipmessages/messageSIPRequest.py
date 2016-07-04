import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class MESSAGESIPRequest(SIPRequest):
    @property
    def isMESSAGERequest(self):
        return True

    @property
    def isKnown(self):
        return True
