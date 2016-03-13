from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPURI


class TestSIPURI(TestCase):
    def test_parseSetValuesAndReParse(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        uri.parameterNamedPut('foo', 42)
        self.assertEqual('sips:8005551212@192.168.0.99:5061;foo=42;user=phone', uri.rawString)
        uri.host = '192.168.0.100'
        self.assertEqual('sips:8005551212@192.168.0.100:5061;foo=42;user=phone', uri.rawString)
        uri.port = 5062
        self.assertEqual('sips:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.scheme = 'sip'
        self.assertEqual('sip:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.user = '8885551212'
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.parameterNamesAndValueStrings = None
        self.assertEqual('sip:8885551212@192.168.0.100:5062', uri.rawString)
        uri.parameterNamedPut('foo', 42)
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42', uri.rawString)
        uri.rawString = uriString
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_setAttributesParseSetValuesAndReParse(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=5061,
                                      scheme='sips',
                                      user='8005551212',
                                      parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        uri.parameterNamedPut('foo', 42)
        self.assertEqual('sips:8005551212@192.168.0.99:5061;foo=42;user=phone', uri.rawString)
        uri.host = '192.168.0.100'
        self.assertEqual('sips:8005551212@192.168.0.100:5061;foo=42;user=phone', uri.rawString)
        uri.port = 5062
        self.assertEqual('sips:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.scheme = 'sip'
        self.assertEqual('sip:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.user = '8885551212'
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42;user=phone', uri.rawString)
        uri.parameterNamesAndValueStrings = None
        self.assertEqual('sip:8885551212@192.168.0.100:5062', uri.rawString)
        uri.parameterNamedPut('foo', 42)
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42', uri.rawString)
        uri.rawString = uriString
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid001(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;user=phone;foo=bar'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('foo'), 'bar')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid002(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid003(self):
        uriString = 'sips:8005551212@192.168.0.99:5061'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid004(self):
        uriString = 'sips:8005551212@192.168.0.99;user=phone;foo=bar'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('foo'), 'bar')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid005(self):
        uriString = 'sips:8005551212@192.168.0.99'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid006(self):
        uriString = 'sips:192.168.0.99:5061;user=phone;foo=bar'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('foo'), 'bar')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_parseValid007(self):
        uriString = 'sips:192.168.0.99'
        uri = SIPURI.newParsedFrom(uriString)
        self.assertEqual(uriString, uri.rawString)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)

    def test_render001(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=5061,
                                      scheme='sips',
                                      user='8005551212',
                                      parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render002(self):
        uriString = 'sips:8005551212@192.168.0.99:5061;foo=bar;user=phone'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=5061,
                                      scheme='sips',
                                      user='8005551212',
                                      parameterNamesAndValueStrings={'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'foo': 'bar', 'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('foo'), 'bar')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render003(self):
        uriString = 'sips:8005551212@192.168.0.99:5061'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=5061,
                                      scheme='sips',
                                      user='8005551212'
                                      )
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render004(self):
        uriString = 'sips:8005551212@192.168.0.99;user=phone'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=None,
                                      scheme='sips',
                                      user='8005551212',
                                      parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameterNamed('user'), 'phone')
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render005(self):
        uriString = 'sips:8005551212@192.168.0.99'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=None,
                                      scheme='sips',
                                      user='8005551212',
                                      )
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render006(self):
        uriString = 'sips:192.168.0.99:5061'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=5061,
                                      scheme='sips',
                                      user=None,
                                      parameterNamesAndValueStrings={})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_render007(self):
        uriString = 'sips:192.168.0.99'
        uri = SIPURI.newForAttributes(host='192.168.0.99',
                                      port=None,
                                      scheme='sips',
                                      user=None,
                                      )
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameterNamed('nonExistentKey'), None)
        self.assertEqual(uriString, uri.rawString)

    def test_usingAnalyzedRealWorldSIPURIs(self):
        # TODO
        pass
