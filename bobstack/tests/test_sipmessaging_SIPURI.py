from unittest import TestCase
import sys
sys.path.append("..")
from sipmessaging import SIPURI


class TestSIPURI(TestCase):
    def test_parseSetValuesAndReParse(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        uri.parameter_named_put('foo', 42)
        self.assertEqual('sips:8005551212@192.168.0.99:5061;foo=42;user=phone', uri.raw_string)
        uri.host = '192.168.0.100'
        self.assertEqual('sips:8005551212@192.168.0.100:5061;foo=42;user=phone', uri.raw_string)
        uri.port = 5062
        self.assertEqual('sips:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.scheme = 'sip'
        self.assertEqual('sip:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.user = '8885551212'
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.parameterNamesAndValueStrings = None
        self.assertEqual('sip:8885551212@192.168.0.100:5062', uri.raw_string)
        uri.parameter_named_put('foo', 42)
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42', uri.raw_string)
        uri.raw_string = uri_string
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_setAttributesParseSetValuesAndReParse(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=5061,
                                        scheme='sips',
                                        user='8005551212',
                                        parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        uri.parameter_named_put('foo', 42)
        self.assertEqual('sips:8005551212@192.168.0.99:5061;foo=42;user=phone', uri.raw_string)
        uri.host = '192.168.0.100'
        self.assertEqual('sips:8005551212@192.168.0.100:5061;foo=42;user=phone', uri.raw_string)
        uri.port = 5062
        self.assertEqual('sips:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.scheme = 'sip'
        self.assertEqual('sip:8005551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.user = '8885551212'
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42;user=phone', uri.raw_string)
        uri.parameterNamesAndValueStrings = None
        self.assertEqual('sip:8885551212@192.168.0.100:5062', uri.raw_string)
        uri.parameter_named_put('foo', 42)
        self.assertEqual('sip:8885551212@192.168.0.100:5062;foo=42', uri.raw_string)
        uri.raw_string = uri_string
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid001(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;user=phone;foo=bar'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('foo'), 'bar')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid002(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid003(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid004(self):
        uri_string = 'sips:8005551212@192.168.0.99;user=phone;foo=bar'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('foo'), 'bar')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid005(self):
        uri_string = 'sips:8005551212@192.168.0.99'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid006(self):
        uri_string = 'sips:192.168.0.99:5061;user=phone;foo=bar'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('foo'), 'bar')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_parseValid007(self):
        uri_string = 'sips:192.168.0.99'
        uri = SIPURI.new_parsed_from(uri_string)
        self.assertEqual(uri_string, uri.raw_string)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)

    def test_render001(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;user=phone'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=5061,
                                        scheme='sips',
                                        user='8005551212',
                                        parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render002(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061;foo=bar;user=phone'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=5061,
                                        scheme='sips',
                                        user='8005551212',
                                        parameterNamesAndValueStrings={'user': 'phone', 'foo': 'bar'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'foo': 'bar', 'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('foo'), 'bar')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render003(self):
        uri_string = 'sips:8005551212@192.168.0.99:5061'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=5061,
                                        scheme='sips',
                                        user='8005551212')
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render004(self):
        uri_string = 'sips:8005551212@192.168.0.99;user=phone'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=None,
                                        scheme='sips',
                                        user='8005551212',
                                        parameterNamesAndValueStrings={'user': 'phone'})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {'user': 'phone'})
        self.assertEqual(uri.parameter_named('user'), 'phone')
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render005(self):
        uri_string = 'sips:8005551212@192.168.0.99'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=None,
                                        scheme='sips',
                                        user='8005551212',)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, '8005551212')
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render006(self):
        uri_string = 'sips:192.168.0.99:5061'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=5061,
                                        scheme='sips',
                                        user=None,
                                        parameterNamesAndValueStrings={})
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, 5061)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_render007(self):
        uri_string = 'sips:192.168.0.99'
        uri = SIPURI.new_for_attributes(host='192.168.0.99',
                                        port=None,
                                        scheme='sips',
                                        user=None,)
        self.assertEqual(uri.host, '192.168.0.99')
        self.assertEqual(uri.port, None)
        self.assertEqual(uri.scheme, 'sips')
        self.assertEqual(uri.user, None)
        self.assertEqual(uri.parameterNamesAndValueStrings, {})
        self.assertEqual(uri.parameter_named('nonExistentKey'), None)
        self.assertEqual(uri_string, uri.raw_string)

    def test_usingAnalyzedRealWorldSIPURIs(self):
        # TODO
        pass
