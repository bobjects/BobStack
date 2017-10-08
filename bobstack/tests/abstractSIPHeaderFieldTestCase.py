try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
# import sys
# sys.path.append("..")
from ..sipmessaging import UnknownSIPHeaderField


class AbstractSIPHeaderFieldTestCase(TestCase):
    @property
    def canonicalStrings(self):
        answer = []
        for field_name in self.canonicalFieldNames + self.canonicalCompactFieldNames:
            for field_value_string in self.canonicalFieldValues:
                answer.append(field_name + ": " + field_value_string)
                answer.append(field_name + ":     " + field_value_string)
                answer.append(field_name + "    : " + field_value_string)
                answer.append(field_name + "    :     " + field_value_string)
        return answer

    @property
    def canonicalFieldNames(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalCompactFieldNames(self):
        name = self.sipHeaderFieldClassUnderTest.canonical_compact_field_name
        if name:
            return [name.lower(), name.upper()]
        else:
            return []

    @property
    def canonicalFieldValues(self):
        return ["baz blarg blonk"]

    @property
    def sipHeaderFieldClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def basic_test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.can_match_string(line))
            self.assertTrue(self.sipHeaderFieldClassUnderTest.can_match_string(line))
            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)
            # print line
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, line)
            self.assertTrue(header_field.field_name.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertTrue(header_field.field_value_string in self.canonicalFieldValues)
            # self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameter_names_and_value_strings, dict)
            header_field.raw_string = self.canonicalFieldNames[0] + ': blooey'
            self.assertEqual("blooey", header_field.field_value_string)
            self.assertEqual(header_field.field_name.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(self.canonicalFieldNames[0] + ': blooey', header_field.raw_string)
            if self.canonicalCompactFieldNames:
                header_field.raw_string = self.canonicalCompactFieldNames[0] + ': blooey'
                self.assertEqual("blooey", header_field.field_value_string)
                self.assertEqual(header_field.field_name.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertEqual(self.canonicalCompactFieldNames[0] + ': blooey', header_field.raw_string)

    def basic_test_rendering(self):
        for field_value_string in self.canonicalFieldValues:
            # TODO:  we will extend this when we implement rendering of compact headers.
            header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)
            self.assertTrue(header_field.is_valid)
            self.assertTrue(header_field.is_known)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': ' + field_value_string)
            header_field.field_value_string = "blooey"
            self.assertEqual("blooey", header_field.field_value_string)
            self.assertEqual(header_field.raw_string, self.canonicalFieldNames[0] + ': blooey')
