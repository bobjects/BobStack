import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class ACKSIPRequest(SIPRequest):
    @property
    def is_ack_request(self):
        return True

    @property
    def is_known(self):
        return True
