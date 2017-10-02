from twisted.protocols import basic
from tcpSIPTwistedProtocol import TCPSIPTwistedProtcol


# TODO:  Maybe not LineReceiver.  We are message-oriented, not line-oriented.
class TCPSIPTwistedServerProtcol(TCPSIPTwistedProtcol, basic.LineReceiver):
    pass
