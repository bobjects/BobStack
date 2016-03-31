from unittest import TestCase
import unittest
import sys
sys.path.append("..")
sys.path.append("../..")
from bobstack.sipmessaging import SIPMessageFactory
from bobstack.siptransport import SimulatedSIPTransport
from bobstack.sipentity import SIPStatelessProxy
from bobstack.siptransport import SimulatedNetwork


class TestStatelessProxy(TestCase):
    def setUp(self):
        SimulatedNetwork.clear()
        self.atlanta = SIPStatelessProxy()
        self.atlanta.transports = [SimulatedSIPTransport(self.atlantaBindAddress, self.atlantaBindPort)]
        self.biloxi = SIPStatelessProxy()
        self.biloxi.transports = [SimulatedSIPTransport(self.biloxiBindAddress, self.biloxiBindPort)]

    def test(self):
        self.run_00_atlanta()
        self.run_01_atlantaToBiloxi()
        self.run_02_biloxiToAtlanta()

    def run_00_atlanta(self):
        pass

    def run_01_atlantaToBiloxi(self):
        pass

    def run_02_biloxiToAtlanta(self):
        pass

    @property
    def atlantaBindAddress(self):
        return '192.168.4.2'

    @property
    def atlantaBindPort(self):
        return 5060

    @property
    def biloxiBindAddress(self):
        return '192.168.4.3'

    @property
    def biloxiBindPort(self):
        return 5060

