# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPRequest
from ...sipmessaging import SIPRequest


class SUBSCRIBESIPRequest(SIPRequest):
    @property
    def is_subscribe_request(self):
        return True

    @property
    def is_known(self):
        return True
