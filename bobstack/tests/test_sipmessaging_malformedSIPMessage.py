from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import MalformedSIPStartLine
from sipmessaging import MalformedSIPMessage
from sipmessaging import ContentLengthSIPHeaderField
from sipmessaging import UnknownSIPHeaderField
from sipmessaging import SIPHeader


class TestMalformedSipMessage(TestCase):
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
            request = MalformedSIPMessage.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 OPTIONS'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = MalformedSIPMessage._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
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


