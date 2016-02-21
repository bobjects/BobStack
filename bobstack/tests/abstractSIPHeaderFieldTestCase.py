try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import inspect
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField



class AbstractSIPHeaderFieldTestCase(TestCase):
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
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line))
            self.assertTrue(self.sipHeaderFieldClassUnderTest.canMatchString(line))
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertTrue(headerField.isValid, line)
            self.assertTrue(headerField.isKnown, line)
            self.assertEqual(headerField.rawString, line, line)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertTrue(headerField.fieldValue in self.canonicalFieldValues)
            headerField.rawString = self.canonicalFieldNames[0] + ': blooey'
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(self.canonicalFieldNames[0] + ': blooey', headerField.rawString)

    def basic_test_rendering(self):
        for fieldValue in self.canonicalFieldValues:
            headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValue=fieldValue)
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': ' + fieldValue)
            headerField.fieldValue = "blooey"
            self.assertEqual("blooey", headerField.fieldValue)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': blooey')
