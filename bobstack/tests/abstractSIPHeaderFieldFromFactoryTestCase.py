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
        for fieldName in self.canonicalFieldNames + self.canonicalCompactFieldNames:
            for fieldValueString in self.canonicalFieldValues:
                answer.append(fieldName + ": " + fieldValueString)
                answer.append(fieldName + ":     " + fieldValueString)
                answer.append(fieldName + "    : " + fieldValueString)
                answer.append(fieldName + "    :     " + fieldValueString)
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
            headerField = SIPHeaderFieldFactory().nextForString(line)
            # print line
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            self.assertTrue('foo' in ['foo', 'bar'])
            self.assertTrue(headerField.fieldName.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(headerField.fieldValueString, basestring, line)
            self.assertTrue(headerField.fieldValueString in self.canonicalFieldValues)

            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            # self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            self.assertTrue(headerField.fieldName.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(headerField.fieldValueString, basestring, line)
            self.assertTrue(headerField.fieldValueString in self.canonicalFieldValues)
            stringio.close()

            # print self.canonicalFieldNames[0]
            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertEqual(self.emptyHeaderFieldBodyIsValid, headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValueString, basestring)
            # self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            if self.canonicalCompactFieldNames:
                headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalCompactFieldNames[0])
                self.assertEqual(self.emptyHeaderFieldBodyIsValid, headerField.isValid)
                self.assertTrue(headerField.isKnown)
                self.assertEqual(headerField.fieldName.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertIsInstance(headerField.fieldValueString, basestring)
                # self.assertNotEqual(headerField.value, None)
                self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)

            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], self.canonicalFieldValues[0])
            self.assertEqual(headerField.fieldValueString, self.canonicalFieldValues[0], line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, self.canonicalStrings[0])
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValueString, basestring, line)
            self.assertTrue(headerField.fieldValueString in self.canonicalFieldValues)
            # self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            if self.canonicalCompactFieldNames:
                headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalCompactFieldNames[0], self.canonicalFieldValues[0])
                self.assertEqual(headerField.fieldValueString, self.canonicalFieldValues[0], line)
                self.assertTrue(headerField.isValid, line)
                self.assertTrue(headerField.isKnown, line)
                self.assertTrue(headerField.rawString in self.canonicalStrings)
                self.assertEqual(headerField.fieldName.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertIsInstance(headerField.fieldValueString, basestring, line)
                self.assertTrue(headerField.fieldValueString in self.canonicalFieldValues)
                # self.assertNotEqual(headerField.value, None)
                self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
