try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import inspect
import sys
sys.path.append("..")
from sipmessaging import SIPHeaderFieldFactory
from abstractSIPHeaderFieldFromFactoryTestCase import AbstractSIPHeaderFieldFromFactoryTestCase


class AbstractIntegerSIPHeaderFieldFromFactoryTestCase(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def sipMethodString(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMessageClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalStartLineStrings(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalFieldValues(self):
        return ["489"]

    def basic_test_parsing(self):
        super(AbstractIntegerSIPHeaderFieldFromFactoryTestCase, self).basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(header_field.field_name.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(header_field.integerValue, (int, long), line)
            self.assertEqual(header_field.integerValue, int(self.canonicalFieldValues[0]))
            header_field.rawString = self.canonicalFieldNames[0] + ': 301'
            self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
            self.assertEqual(301, header_field.integerValue)
            self.assertEqual(header_field.field_name.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(header_field.field_value_string, "301")
            self.assertEqual(self.canonicalFieldNames[0] + ': 301', header_field.rawString)
            if self.canonicalCompactFieldNames:
                header_field.rawString = self.canonicalCompactFieldNames[0] + ': 301'
                self.assertNotEqual(header_field.value, None)
                self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
                self.assertEqual(301, header_field.integerValue)
                self.assertEqual(header_field.field_name.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertEqual(header_field.field_value_string, "301")
                self.assertEqual(self.canonicalCompactFieldNames[0] + ': 301', header_field.rawString)

