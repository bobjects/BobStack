import sys
sys.path.append("../../..")
from bobstack.sipmessaging import SIPRequest


class UPDATESIPRequest(SIPRequest):
    @property
    def isUPDATERequest(self):
        return True

    @property
    def isKnown(self):
        return True
