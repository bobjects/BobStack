from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.unknownSIPRequest import UnknownSIPRequest
from sipmessaging.optionsSIPRequest import OPTIONSSIPRequest
from sipmessaging.contentLengthSIPHeaderField import ContentLengthSIPHeaderField


class TestUnknownSIPRequest(TestCase):
    pass


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
             'Content-Length:     11\r\n'
             '\r\n'
             'Foo Content')
        ]

    def test_parsing(self):
        for messageString in self.canonicalStrings:
            request = OPTIONSSIPRequest(stringToParse=messageString)
            # print [x.rawString for x in request.headerFields]
            self.assertTrue(request.isKnown)
            self.assertTrue(request.isValid)
            self.assertTrue(request.isRequest)
            self.assertFalse(request.isResponse)
            self.assertTrue(request.isKnown)
            self.assertTrue(request.isOPTIONSRequest)
            self.assertFalse(request.isMalformed)
            self.assertEqual(1, [headerField for headerField in request.headerFields if headerField.isContentLength].__len__())
            self.assertEqual(11, next(headerField for headerField in request.headerFields if headerField.isContentLength).value)
            self.assertEqual(10, [headerField for headerField in request.headerFields if headerField.isUnknown].__len__())
            self.assertTrue(request.startLine.isRequest)
            self.assertEqual('Foo Content', request.content)
            self.assertEqual('OPTIONS', request.startLine.sipMethod)
            self.assertEqual('sip:example.com', request.startLine.requestURI)

    def test_rendering(self):
        # TODO
        pass

