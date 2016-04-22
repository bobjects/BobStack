try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import inspect
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField
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
            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.integerValue, (int, long))
            self.assertEqual(headerField.integerValue, int(self.canonicalFieldValues[0]))
            headerField.rawString = self.canonicalFieldNames[0] + ': 301'
            self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            self.assertEqual(301, headerField.integerValue)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(headerField.fieldValueString, "301")
            self.assertEqual(self.canonicalFieldNames[0] + ': 301', headerField.rawString)

    def basic_test_rendering(self):
        # super(AbstractIntegerSIPHeaderFieldTestCase, self).basic_test_rendering()
        for fieldValueString in self.canonicalFieldValues:
            headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(value=300)
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': 300')
            self.assertIsInstance(headerField.integerValue, (int, long))
            self.assertEqual(headerField.integerValue, 300)
            self.assertEqual("300", headerField.fieldValueString)
            headerField.fieldValueString = "500"
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': 500')
            self.assertIsInstance(headerField.integerValue, (int, long))
            self.assertEqual(headerField.integerValue, 500)
            self.assertEqual("500", headerField.fieldValueString)
            headerField.integerValue = 501
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': 501')
            self.assertIsInstance(headerField.integerValue, (int, long))
            self.assertEqual(headerField.integerValue, 501)
            self.assertEqual("501", headerField.fieldValueString)
            headerField = self.sipHeaderFieldClassUnderTest.newForIntegerValue(300)
            self.assertTrue(headerField.isValid)
            self.assertTrue(headerField.isKnown)
            self.assertEqual(headerField.rawString, self.canonicalFieldNames[0] + ': 300')
            self.assertIsInstance(headerField.integerValue, (int, long))
            self.assertEqual(headerField.integerValue, 300)
            self.assertEqual("300", headerField.fieldValueString)
