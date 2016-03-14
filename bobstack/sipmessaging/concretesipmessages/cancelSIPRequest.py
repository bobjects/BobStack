import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class CANCELSIPRequest(SIPRequest):
    @property
    def isCANCELRequest(self):
        return True

    @property
    def isKnown(self):
        return True
