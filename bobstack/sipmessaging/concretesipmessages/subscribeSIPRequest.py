import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class SUBSCRIBESIPRequest(SIPRequest):
    @property
    def isSUBSCRIBERequest(self):
        return True

    @property
    def isKnown(self):
        return True
