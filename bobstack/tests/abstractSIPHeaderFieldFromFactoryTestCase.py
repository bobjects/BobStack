try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField
from sipmessaging import SIPHeaderFieldFactory



class AbstractSIPHeaderFieldFromFactoryTestCase(TestCase):
    @property
    def canonicalStrings(self):
        answer = []
        for fieldName in self.canonicalFieldNames:
            for fieldValue in self.canonicalFieldValues:
                answer.append(fieldName + ": " + fieldValue)
                answer.append(fieldName + ":     " + fieldValue)
                answer.append(fieldName + "    : " + fieldValue)
                answer.append(fieldName + "    :     " + fieldValue)
        return answer

    @property
    def canonicalFieldNames(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalFieldValues(self):
        return ["baz blarg blonk"]

    @property
    def sipHeaderFieldClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def basic_test_parsing(self):
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertTrue(headerField.fieldValue in self.canonicalFieldValues)

            stringio = StringIO(line + '\r\n')
            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertTrue(headerField.fieldValue in self.canonicalFieldValues)
            stringio.close()

            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValue, basestring)

            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], self.canonicalFieldValues[0])
            self.assertEqual(headerField.fieldValue, self.canonicalFieldValues[0], line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, self.canonicalStrings[0])
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.fieldValue, basestring, line)
            self.assertTrue(headerField.fieldValue in self.canonicalFieldValues)
