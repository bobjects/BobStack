from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.sipMessageFactory import SIPMessageFactory


class TestSIPMessageFactoryForMalformedSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('Malformed start line\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 OPTIONS\r\n'
             'Max-Forwards: 70\r\n'
             'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
             'User-Agent: Example User Agent\r\n'
             'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
             'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
             'Expires: 0\r\n'
             'Content-Length: 11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            request = SIPMessageFactory().nextForString(messageString)
            self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isValid)
        self.assertFalse(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertTrue(aSIPRequest.isMalformed)
        self.assertIsNotNone(aSIPRequest.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPRequest.header.contentLength)
        self.assertEqual(10, aSIPRequest.header.unknownHeaderFields.__len__())
        self.assertFalse(aSIPRequest.startLine.isRequest)
        self.assertFalse(aSIPRequest.startLine.isResponse)
        self.assertTrue(aSIPRequest.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPRequest.content)
        self.assertEqual('Malformed start line', aSIPRequest.startLine.rawString)


class TestSIPMessageFactoryForUnknownSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('UNKNOWN sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 OPTIONS\r\n'
             'Max-Forwards: 70\r\n'
             'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
             'User-Agent: Example User Agent\r\n'
             'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
             'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
             'Expires: 0\r\n'
             'Content-Length: 11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            request = SIPMessageFactory().nextForString(messageString)
            self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isMalformed)
        # self.assertEqual(1, [headerField for headerField in aSIPRequest.header.headerFields if headerField.isContentLength].__len__())
        # self.assertEqual(11, next(headerField for headerField in aSIPRequest.header.headerFields if headerField.isContentLength).value)
        # self.assertEqual(10, [headerField for headerField in aSIPRequest.header.headerFields if headerField.isUnknown].__len__())
        self.assertIsNotNone(aSIPRequest.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPRequest.header.contentLength)
        self.assertEqual(10, aSIPRequest.header.unknownHeaderFields.__len__())
        self.assertTrue(aSIPRequest.startLine.isRequest)
        self.assertFalse(aSIPRequest.startLine.isResponse)
        self.assertFalse(aSIPRequest.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPRequest.content)
        self.assertEqual('UNKNOWN', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestSIPMessageFactoryForOPTIONSSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('OPTIONS sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 OPTIONS\r\n'
             'Max-Forwards: 70\r\n'
             'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
             'User-Agent: Example User Agent\r\n'
             'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
             'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
             'Expires: 0\r\n'
             'Content-Length: 11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            request = SIPMessageFactory().nextForString(messageString)
            self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertTrue(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isMalformed)
        # self.assertEqual(1, [headerField for headerField in aSIPRequest.header.headerFields if headerField.isContentLength].__len__())
        # self.assertEqual(11, next(headerField for headerField in aSIPRequest.header.headerFields if headerField.isContentLength).value)
        # self.assertEqual(10, [headerField for headerField in aSIPRequest.header.headerFields if headerField.isUnknown].__len__())
        self.assertIsNotNone(aSIPRequest.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPRequest.header.contentLength)
        self.assertEqual(10, aSIPRequest.header.unknownHeaderFields.__len__())
        self.assertTrue(aSIPRequest.startLine.isRequest)
        self.assertFalse(aSIPRequest.startLine.isResponse)
        self.assertFalse(aSIPRequest.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPRequest.content)
        self.assertEqual('OPTIONS', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestSIPMessageFactoryForSIPResponse(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('SIP/2.0 100 Trying\r\n'
             'From: "3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518\r\n'
             'To: "3125551313"<sip:3125551313@example.com:5064;user=phone>\r\n'
             'Call-ID: a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241\r\n'
             'CSeq: 615 INVITE\r\n'
             'Via: SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8\r\n'
             'Content-Length: 11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            response = SIPMessageFactory().nextForString(messageString)
            self.runAssertionsForResponse(response)

    def test_eventTriggering(self):
        # TODO
        pass

    def runAssertionsForResponse(self, aSIPResponse):
        self.assertEqual(aSIPResponse.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPResponse.isKnown)
        self.assertFalse(aSIPResponse.isUnknown)
        self.assertTrue(aSIPResponse.isValid)
        self.assertFalse(aSIPResponse.isRequest)
        self.assertTrue(aSIPResponse.isResponse)
        self.assertFalse(aSIPResponse.isOPTIONSRequest)
        self.assertFalse(aSIPResponse.isMalformed)
        # self.assertEqual(1, [headerField for headerField in aSIPResponse.header.headerFields if headerField.isContentLength].__len__())
        # self.assertEqual(11, next(headerField for headerField in aSIPResponse.header.headerFields if headerField.isContentLength).value)
        # self.assertEqual(5, [headerField for headerField in aSIPResponse.header.headerFields if headerField.isUnknown].__len__())
        self.assertIsNotNone(aSIPResponse.header.contentLengthHeaderField)
        self.assertEqual(11, aSIPResponse.header.contentLength)
        self.assertEqual(5, aSIPResponse.header.unknownHeaderFields.__len__())
        self.assertTrue(aSIPResponse.startLine.isResponse)
        self.assertFalse(aSIPResponse.startLine.isRequest)
        self.assertFalse(aSIPResponse.startLine.isMalformed)
        self.assertEqual('Foo Content', aSIPResponse.content)
        self.assertEqual(100, aSIPResponse.startLine.statusCode)
        self.assertEqual('Trying', aSIPResponse.startLine.reasonPhrase)




