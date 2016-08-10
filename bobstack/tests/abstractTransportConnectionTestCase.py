from unittest import TestCase
import sys
sys.path.append("..")
sys.path.append("../..")
from bobstack.sipmessaging import SIPURI
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.sipentity import SIPStatelessProxy
from bobstack.siptransport import SimulatedNetwork

class AbstractTransportConnectionTestCase(TestCase):
    # We will be refactoring most of the test behavior down to here, and override
    # to test different transports as we implement them.
    pass