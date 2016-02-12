import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPRequest


class OPTIONSSIPRequest(SIPRequest):
    @property
    def isOPTIONSRequest(self):
        return True

    @property
    def isKnown(self):
        return True
