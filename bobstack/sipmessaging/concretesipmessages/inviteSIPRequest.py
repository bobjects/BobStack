import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPRequest


class INVITESIPRequest(SIPRequest):
    @property
    def isINVITERequest(self):
        return True

    @property
    def isKnown(self):
        return True
