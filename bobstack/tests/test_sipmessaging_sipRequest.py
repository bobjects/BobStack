from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.unknownSIPRequest import UnknownSIPRequest
from sipmessaging.optionsSIPRequest import OPTIONSSIPRequest
from sipmessaging.sipHeader import SIPHeader
from sipmessaging.contentLengthSIPHeaderField import ContentLengthSIPHeaderField
from sipmessaging.unknownSIPHeaderField import UnknownSIPHeaderField
# from sipmessaging.sipRequestStartLine import SIPRequestStartLine


class TestUnknownSIPRequest(TestCase):
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
            request = UnknownSIPRequest(stringToParse=messageString)
            self.runAssertionsForRequest(request)

    def test_rendering(self):
        headerFields = [
            UnknownSIPHeaderField(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField(fieldName='CSeq', fieldValue='6711 OPTIONS'),
            UnknownSIPHeaderField(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField(value=11)]
        request = UnknownSIPRequest(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader(headerFields=headerFields))
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


class TestOPTIONSSIPRequest(TestCase):
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
            request = OPTIONSSIPRequest(stringToParse=messageString)
            self.runAssertionsForRequest(request)

    def test_rendering(self):
        headerFields = [
            UnknownSIPHeaderField(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField(fieldName='CSeq', fieldValue='6711 OPTIONS'),
            UnknownSIPHeaderField(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField(value=11)]
        request = OPTIONSSIPRequest(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader(headerFields=headerFields))
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
        self.assertEqual('Foo Content', aSIPRequest.content)
        self.assertEqual('OPTIONS', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)
