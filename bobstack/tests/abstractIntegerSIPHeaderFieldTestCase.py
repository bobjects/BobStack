try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import inspect
import sys
sys.path.append("..")
from abstractSIPHeaderFieldTestCase import AbstractSIPHeaderFieldTestCase


class AbstractIntegerSIPHeaderFieldTestCase(AbstractSIPHeaderFieldTestCase):
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
        super(AbstractIntegerSIPHeaderFieldTestCase, self).basic_test_parsing()
        for line in self.canonicalStrings:
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            self.assertTrue(header_field.field_name.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(header_field.integer_value, (int, long))
            self.assertEqual(header_field.integer_value, int(self.canonicalFieldValues[0]))
            header_field.raw_string = self.canonicalFieldNames[0] + ': 301'
            self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameter_names_and_value_strings, dict)
            self.assertEqual(301, header_field.integer_value)
            self.assertEqual(header_field.field_name.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(header_field.field_value_string, "301")
            self.assertEqual(self.canonicalFieldNames[0] + ': 301', header_field.raw_string)
            if self.canonicalCompactFieldNames:
                header_field.raw_string = self.canonicalCompactFieldNames[0] + ': 301'
                self.assertNotEqual(header_field.value, None)
                self.assertIsInstance(header_field.parameter_names_and_value_strings, dict)
                self.assertEqual(301, header_field.integer_value)
                self.assertEqual(header_field.field_name.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertEqual(header_field.field_value_string, "301")
                self.assertEqual(self.canonicalCompactFieldNames[0] + ': 301', header_field.raw_string)

    def basic_test_rendering(self):
        # super(AbstractIntegerSIPHeaderFieldTestCase, self).basic_test_rendering()
        for field_value_string in self.canonicalFieldValues:
            # TODO:  we will extend this for rendering with compact header field names.
            header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(value=300)
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': 300')
            self.assertIsInstance(header_field.integer_value, (int, long))
            self.assertEqual(header_field.integer_value, 300)
            self.assertEqual("300", header_field.field_value_string)
            header_field.field_value_string = "500"
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': 500')
            self.assertIsInstance(header_field.integer_value, (int, long))
            self.assertEqual(header_field.integer_value, 500)
            self.assertEqual("500", header_field.field_value_string)
            header_field.integer_value = 501
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': 501')
            self.assertIsInstance(header_field.integer_value, (int, long))
            self.assertEqual(header_field.integer_value, 501)
            self.assertEqual("501", header_field.field_value_string)
            header_field = self.sipHeaderFieldClassUnderTest.new_for_integer_value(300)
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': 300')
            self.assertIsInstance(header_field.integer_value, (int, long))
            self.assertEqual(header_field.integer_value, 300)
            self.assertEqual("300", header_field.field_value_string)
