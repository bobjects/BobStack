from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import StrongRandomStringServer

class test_StrongRandomStringServer(TestCase):
    def testIt(self):
        server = StrongRandomStringServer()
        for i in xrange(10000):
            randomString = server.next32Bits
            self.assertIsInstance(randomString, basestring)
            self.assertTrue(len(randomString) == 8)
            # print randomString

    def testSingleton(self):
        for i in xrange(10000):
            randomString = StrongRandomStringServer.instance.next32Bits
            self.assertIsInstance(randomString, basestring)
            self.assertTrue(len(randomString) == 8)
            # print randomString
