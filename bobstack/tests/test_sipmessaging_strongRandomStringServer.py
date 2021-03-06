from unittest import TestCase
from ..sipmessaging import StrongRandomStringServer


class TestStrongRandomStringServer(TestCase):
    def testIt(self):
        server = StrongRandomStringServer()
        for i in xrange(10000):
            random_string = server.next_32_bits
            self.assertIsInstance(random_string, basestring)
            self.assertTrue(len(random_string) == 8)
            # print random_string

    def testSingleton(self):
        for i in xrange(10000):
            random_string = StrongRandomStringServer.instance.next_32_bits
            self.assertIsInstance(random_string, basestring)
            self.assertTrue(len(random_string) == 8)
            # print random_string
