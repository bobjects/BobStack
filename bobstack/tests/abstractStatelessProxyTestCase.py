from unittest import TestCase
from ..sipmessaging import SIPURI
from ..siptransport import SimulatedSIPTransport
from ..sipentity import SIPStatelessProxy
from ..siptransport import SimulatedNetwork


class AbstractStatelessProxyTestCase(TestCase):
    # We will be refactoring most of the test behavior down to here, and override
    # to test different transports as we implement them.
    pass
