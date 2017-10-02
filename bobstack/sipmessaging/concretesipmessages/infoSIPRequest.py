import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPRequest
from sipmessaging import SIPRequest


class INFOSIPRequest(SIPRequest):
    @property
    def is_info_request(self):
        return True

    @property
    def is_known(self):
        return True
