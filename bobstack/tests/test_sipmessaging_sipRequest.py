from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPRequest
from sipmessaging import ACKSIPRequest
from sipmessaging import BYESIPRequest
from sipmessaging import CANCELSIPRequest
from sipmessaging import INFOSIPRequest
from sipmessaging import INVITESIPRequest
from sipmessaging import NOTIFYSIPRequest
from sipmessaging import OPTIONSSIPRequest
from sipmessaging import REFERSIPRequest
from sipmessaging import REGISTERSIPRequest
from sipmessaging import SUBSCRIBESIPRequest
from sipmessaging import UPDATESIPRequest
from sipmessaging import SIPHeader
from sipmessaging import ContentLengthSIPHeaderField
from sipmessaging import UnknownSIPHeaderField
# from sipmessaging import SIPRequestStartLine


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
            request = UnknownSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
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
        request = UnknownSIPRequest.newForAttributes(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 OPTIONS\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UnknownSIPRequest.newForAttributes(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 OPTIONS',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UnknownSIPRequest.newForAttributes(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 OPTIONS'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', 11)]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        # , and could alternatively be specified as ('Content-Length', {'value': 11}) which would invoke the value setter on the ContentLengthSIPHeaderField instance
        request = UnknownSIPRequest.newForAttributes(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_including_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 OPTIONS'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UnknownSIPRequest.newForAttributes(sipMethod='UNKNOWN', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
            request = OPTIONSSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
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
        request = OPTIONSSIPRequest.newForAttributes(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 OPTIONS\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = OPTIONSSIPRequest.newForAttributes(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 OPTIONS',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = OPTIONSSIPRequest.newForAttributes(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 OPTIONS'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = OPTIONSSIPRequest.newForAttributes(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 OPTIONS'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = OPTIONSSIPRequest.newForAttributes(sipMethod='OPTIONS', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertTrue(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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


class TestACKSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('ACK sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 ACK\r\n'
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
            request = ACKSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 ACK'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = ACKSIPRequest.newForAttributes(sipMethod='ACK', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 ACK\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = ACKSIPRequest.newForAttributes(sipMethod='ACK', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 ACK',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = ACKSIPRequest.newForAttributes(sipMethod='ACK', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 ACK'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = ACKSIPRequest.newForAttributes(sipMethod='ACK', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 ACK'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = ACKSIPRequest.newForAttributes(sipMethod='ACK', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertTrue(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('ACK', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestBYESIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('BYE sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 BYE\r\n'
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
            request = BYESIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 BYE'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = BYESIPRequest.newForAttributes(sipMethod='BYE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 BYE\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = BYESIPRequest.newForAttributes(sipMethod='BYE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 BYE',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = BYESIPRequest.newForAttributes(sipMethod='BYE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 BYE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = BYESIPRequest.newForAttributes(sipMethod='BYE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 BYE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = BYESIPRequest.newForAttributes(sipMethod='BYE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertTrue(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('BYE', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestCANCELSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('CANCEL sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 CANCEL\r\n'
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
            request = CANCELSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 CANCEL'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = CANCELSIPRequest.newForAttributes(sipMethod='CANCEL', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 CANCEL\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = CANCELSIPRequest.newForAttributes(sipMethod='CANCEL', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 CANCEL',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = CANCELSIPRequest.newForAttributes(sipMethod='CANCEL', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 CANCEL'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = CANCELSIPRequest.newForAttributes(sipMethod='CANCEL', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 CANCEL'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = CANCELSIPRequest.newForAttributes(sipMethod='CANCEL', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertTrue(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('CANCEL', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestINFOSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('INFO sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 INFO\r\n'
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
            request = INFOSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 INFO'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = INFOSIPRequest.newForAttributes(sipMethod='INFO', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 INFO\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INFOSIPRequest.newForAttributes(sipMethod='INFO', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 INFO',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INFOSIPRequest.newForAttributes(sipMethod='INFO', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 INFO'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INFOSIPRequest.newForAttributes(sipMethod='INFO', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 INFO'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INFOSIPRequest.newForAttributes(sipMethod='INFO', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertTrue(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('INFO', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestINVITESIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('INVITE sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 INVITE\r\n'
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
            request = INVITESIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 INVITE'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = INVITESIPRequest.newForAttributes(sipMethod='INVITE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 INVITE\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INVITESIPRequest.newForAttributes(sipMethod='INVITE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 INVITE',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INVITESIPRequest.newForAttributes(sipMethod='INVITE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 INVITE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INVITESIPRequest.newForAttributes(sipMethod='INVITE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 INVITE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = INVITESIPRequest.newForAttributes(sipMethod='INVITE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertTrue(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('INVITE', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestNOTIFYSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('NOTIFY sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 NOTIFY\r\n'
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
            request = NOTIFYSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 NOTIFY'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = NOTIFYSIPRequest.newForAttributes(sipMethod='NOTIFY', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 NOTIFY\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = NOTIFYSIPRequest.newForAttributes(sipMethod='NOTIFY', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 NOTIFY',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = NOTIFYSIPRequest.newForAttributes(sipMethod='NOTIFY', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 NOTIFY'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = NOTIFYSIPRequest.newForAttributes(sipMethod='NOTIFY', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 NOTIFY'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = NOTIFYSIPRequest.newForAttributes(sipMethod='NOTIFY', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertTrue(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('NOTIFY', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestREFERSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('REFER sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 REFER\r\n'
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
            request = REFERSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 REFER'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = REFERSIPRequest.newForAttributes(sipMethod='REFER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 REFER\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REFERSIPRequest.newForAttributes(sipMethod='REFER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 REFER',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REFERSIPRequest.newForAttributes(sipMethod='REFER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 REFER'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REFERSIPRequest.newForAttributes(sipMethod='REFER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 REFER'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REFERSIPRequest.newForAttributes(sipMethod='REFER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertTrue(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('REFER', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestREGISTERSIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('REGISTER sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 REGISTER\r\n'
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
            request = REGISTERSIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 REGISTER'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = REGISTERSIPRequest.newForAttributes(sipMethod='REGISTER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 REGISTER\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REGISTERSIPRequest.newForAttributes(sipMethod='REGISTER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 REGISTER',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REGISTERSIPRequest.newForAttributes(sipMethod='REGISTER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 REGISTER'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REGISTERSIPRequest.newForAttributes(sipMethod='REGISTER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 REGISTER'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = REGISTERSIPRequest.newForAttributes(sipMethod='REGISTER', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertTrue(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('REGISTER', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestSUBSCRIBESIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('SUBSCRIBE sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 SUBSCRIBE\r\n'
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
            request = SUBSCRIBESIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 SUBSCRIBE'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = SUBSCRIBESIPRequest.newForAttributes(sipMethod='SUBSCRIBE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 SUBSCRIBE\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = SUBSCRIBESIPRequest.newForAttributes(sipMethod='SUBSCRIBE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 SUBSCRIBE',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = SUBSCRIBESIPRequest.newForAttributes(sipMethod='SUBSCRIBE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 SUBSCRIBE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = SUBSCRIBESIPRequest.newForAttributes(sipMethod='SUBSCRIBE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 SUBSCRIBE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = SUBSCRIBESIPRequest.newForAttributes(sipMethod='SUBSCRIBE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertTrue(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('SUBSCRIBE', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)


class TestUPDATESIPRequest(TestCase):
    @property
    def canonicalStrings(self):
        return [
            ('UPDATE sip:example.com SIP/2.0\r\n'
             'From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
             'To: <sip:example.com:5061>\r\n'
             'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
             'CSeq: 6711 UPDATE\r\n'
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
            request = UPDATESIPRequest.newParsedFrom(messageString)
            self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_fields(self):
        headerFields = [
            UnknownSIPHeaderField.newForAttributes(fieldName='From', fieldValue='<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='To', fieldValue='<sip:example.com:5061>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Call-ID', fieldValue='0ee8d3e272e31c9195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='CSeq', fieldValue='6711 UPDATE'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Max-Forwards', fieldValue='70'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Via', fieldValue='SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
            UnknownSIPHeaderField.newForAttributes(fieldName='User-Agent', fieldValue='Example User Agent'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Contact', fieldValue='<sip:invalid@200.25.3.150:5061;transport=tls>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Route', fieldValue='<sip:200.30.10.12:5061;transport=tls;lr>'),
            UnknownSIPHeaderField.newForAttributes(fieldName='Expires', fieldValue='0'),
            ContentLengthSIPHeaderField.newForAttributes(value=11)]
        request = UPDATESIPRequest.newForAttributes(sipMethod='UPDATE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_one_big_header_strings(self):
        headerFields = ('From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500\r\n'
                        'To: <sip:example.com:5061>\r\n'
                        'Call-ID: 0ee8d3e272e31c9195299efc500\r\n'
                        'CSeq: 6711 UPDATE\r\n'
                        'Max-Forwards: 70\r\n'
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500\r\n'
                        'User-Agent: Example User Agent\r\n'
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>\r\n'
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>\r\n'
                        'Expires: 0\r\n'
                        'Content-Length: 11')  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UPDATESIPRequest.newForAttributes(sipMethod='UPDATE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_header_field_strings(self):
        headerFields = ['From: <sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500',
                        'To: <sip:example.com:5061>',
                        'Call-ID: 0ee8d3e272e31c9195299efc500',
                        'CSeq: 6711 UPDATE',
                        'Max-Forwards: 70',
                        'Via: SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500',
                        'User-Agent: Example User Agent',
                        'Contact: <sip:invalid@200.25.3.150:5061;transport=tls>',
                        'Route: <sip:200.30.10.12:5061;transport=tls;lr>',
                        'Expires: 0',
                        'Content-Length: 11']  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UPDATESIPRequest.newForAttributes(sipMethod='UPDATE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 UPDATE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UPDATESIPRequest.newForAttributes(sipMethod='UPDATE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = [('From', '<sip:200.25.3.150:5061>;tag=0ee8d3e272e31c9195299efc500'),
                        ('To', '<sip:example.com:5061>'),
                        ('Call-ID', '0ee8d3e272e31c9195299efc500'),
                        ('CSeq', '6711 UPDATE'),
                        ('Max-Forwards', 70),  # note the integer value.
                        ('Via', 'SIP/2.0/TLS 200.25.3.150;branch=z9hG4bK0ee8d3e272e31ca195299efc500'),
                        ('User-Agent', 'Example User Agent'),
                        ('Contact', '<sip:invalid@200.25.3.150:5061;transport=tls>'),
                        ('Route', '<sip:200.30.10.12:5061;transport=tls;lr>'),
                        ('Expires', 0),
                        ('Content-Length', {"value": 11})]  # This last one actually instantiates a ContentLengthSIPHeaderField.
        request = UPDATESIPRequest.newForAttributes(sipMethod='UPDATE', requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForRequest(request)

    def runAssertionsForRequest(self, aSIPRequest):
        self.assertEqual(aSIPRequest.rawString, self.canonicalStrings[0])
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isValid)
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isResponse)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertTrue(aSIPRequest.isUPDATERequest)
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
        self.assertEqual('UPDATE', aSIPRequest.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPRequest.startLine.requestURI)
