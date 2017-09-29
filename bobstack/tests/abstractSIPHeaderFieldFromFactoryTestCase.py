try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
import sys
sys.path.append("..")
from sipmessaging import SIPHeaderFieldFactory


class AbstractSIPHeaderFieldFromFactoryTestCase(TestCase):
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
        name = self.sipHeaderFieldClassUnderTest.canonicalCompactFieldName
        if name:
            return [name.lower(), name.upper()]
        else:
            return []

    @property
    def canonicalFieldValues(self):
        return ["baz blarg blonk"]

    @property
    def emptyHeaderFieldBodyIsValid(self):
        return True

    @property
    def sipHeaderFieldClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def basic_test_parsing(self):
        for line in self.canonicalStrings:
            header_field = SIPHeaderFieldFactory().nextForString(line)
            # print line
            self.assertTrue(header_field.isValid, line)
            self.assertTrue(header_field.isKnown, line)
            self.assertEqual(header_field.rawString, line, line)
            # self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
            self.assertTrue('foo' in ['foo', 'bar'])
            self.assertTrue(header_field.field_name.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(header_field.field_value_string, basestring, line)
            self.assertTrue(header_field.field_value_string in self.canonicalFieldValues)

            stringio = StringIO(line + '\r\n')
            header_field = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(header_field.isValid, line)
            self.assertTrue(header_field.isKnown, line)
            self.assertEqual(header_field.rawString, line, line)
            # self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
            self.assertTrue(header_field.field_name.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(header_field.field_value_string, basestring, line)
            self.assertTrue(header_field.field_value_string in self.canonicalFieldValues)
            stringio.close()

            # print self.canonicalFieldNames[0]
            header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertEqual(self.emptyHeaderFieldBodyIsValid, header_field.isValid)
            self.assertTrue(header_field.isKnown)
            self.assertEqual(header_field.field_name.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(header_field.field_value_string, basestring)
            # self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
            if self.canonicalCompactFieldNames:
                header_field = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
                self.assertEqual(self.emptyHeaderFieldBodyIsValid, header_field.isValid)
                self.assertTrue(header_field.isKnown)
                self.assertEqual(header_field.field_name.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertIsInstance(header_field.field_value_string, basestring)
                # self.assertNotEqual(header_field.value, None)
                self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)

            header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], self.canonicalFieldValues[0])
            self.assertEqual(header_field.field_value_string, self.canonicalFieldValues[0], line)
            self.assertTrue(header_field.isValid, line)
            self.assertTrue(header_field.isKnown, line)
            self.assertEqual(header_field.rawString, self.canonicalStrings[0])
            self.assertEqual(header_field.field_name.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(header_field.field_value_string, basestring, line)
            self.assertTrue(header_field.field_value_string in self.canonicalFieldValues)
            # self.assertNotEqual(header_field.value, None)
            self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
            if self.canonicalCompactFieldNames:
                header_field = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], self.canonicalFieldValues[0])
                self.assertEqual(header_field.field_value_string, self.canonicalFieldValues[0], line)
                self.assertTrue(header_field.isValid, line)
                self.assertTrue(header_field.isKnown, line)
                self.assertTrue(header_field.rawString in self.canonicalStrings)
                self.assertEqual(header_field.field_name.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertIsInstance(header_field.field_value_string, basestring, line)
                self.assertTrue(header_field.field_value_string in self.canonicalFieldValues)
                # self.assertNotEqual(header_field.value, None)
                self.assertIsInstance(header_field.parameterNamesAndValueStrings, dict)
