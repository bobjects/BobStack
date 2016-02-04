from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging.sipResponse import SIPResponse
from sipmessaging.sipHeader import SIPHeader
from sipmessaging.contentLengthSIPHeaderField import ContentLengthSIPHeaderField
from sipmessaging.unknownSIPHeaderField import UnknownSIPHeaderField
# from sipmessaging.sipResponseStartLine import SIPResponseStartLine


class TestSIPResponse(TestCase):
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
            response = SIPResponse(stringToParse=messageString)
            self.runAssertionsForResponse(response)

    def test_rendering(self):
        headerFields = [
            UnknownSIPHeaderField(fieldName='From', fieldValue='"3125551212"<sip:3125551212@example.com:5064;user=phone>;tag=e95a00000022137fe518'),
            UnknownSIPHeaderField(fieldName='To', fieldValue='"3125551313"<sip:3125551313@example.com:5064;user=phone>'),
            UnknownSIPHeaderField(fieldName='Call-ID', fieldValue='a12d6210342b0183745ef9750992682d90d7edce@200.23.3.241'),
            UnknownSIPHeaderField(fieldName='CSeq', fieldValue='615 INVITE'),
            # UnknownSIPHeaderField(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField(fieldName='Via', fieldValue='SIP/2.0/UDP 200.23.3.241:5064;received=200.30.10.15;branch=z9hG4bK-3f04bd-f62a8381-4ebadacb-0x692748a8'),
            ContentLengthSIPHeaderField(value=11)]
        response = SIPResponse(statusCode=100, reasonPhrase='Trying', content='Foo Content', header=SIPHeader(headerFields=headerFields))
        self.runAssertionsForResponse(response)

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



