import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class PRACKSIPRequest(SIPRequest):
    @property
    def is_prack_request(self):
        return True

    @property
    def is_known(self):
        return True
