from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPRequest
from sipmessaging import OPTIONSSIPRequest
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
