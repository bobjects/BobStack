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
    def sipHeaderFieldClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def basic_test_parsing(self):
        for line in self.canonicalStrings:
            self.assertFalse(UnknownSIPHeaderField.canMatchString(line))
            self.assertTrue(self.sipHeaderFieldClassUnderTest.canMatchString(line))
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            # print line
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, line)
            self.assertTrue(headerField.fieldName.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertTrue(headerField.fieldValueString in self.canonicalFieldValues)
            # self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            headerField.rawString = self.canonicalFieldNames[0] + ': blooey'
            self.assertEqual("blooey", headerField.fieldValueString)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(self.canonicalFieldNames[0] + ': blooey', headerField.rawString)
            if self.canonicalCompactFieldNames:
                headerField.rawString = self.canonicalCompactFieldNames[0] + ': blooey'
                self.assertEqual("blooey", headerField.fieldValueString)
                self.assertEqual(headerField.fieldName.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertEqual(self.canonicalCompactFieldNames[0] + ': blooey', headerField.rawString)

    def basic_test_rendering(self):
        for fieldValueString in self.canonicalFieldValues:
            # TODO:  we will extend this when we implement rendering of compact headers.
            headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': ' + fieldValueString)
            headerField.fieldValueString = "blooey"
            self.assertEqual("blooey", headerField.fieldValueString)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': blooey')
