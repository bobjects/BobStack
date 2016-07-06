try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import inspect
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPHeaderField
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
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertTrue(headerField.fieldName.lower() in [name.lower() for name in self.canonicalFieldNames] + [name.lower() for name in self.canonicalCompactFieldNames])
            self.assertIsInstance(headerField.integerValue, (int, long), line)
            self.assertEqual(headerField.integerValue, int(self.canonicalFieldValues[0]))
            headerField.rawString = self.canonicalFieldNames[0] + ': 301'
            self.assertNotEqual(headerField.value, None)
            self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
            self.assertEqual(301, headerField.integerValue)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(headerField.fieldValueString, "301")
            self.assertEqual(self.canonicalFieldNames[0] + ': 301', headerField.rawString)
            if self.canonicalCompactFieldNames:
                headerField.rawString = self.canonicalCompactFieldNames[0] + ': 301'
                self.assertNotEqual(headerField.value, None)
                self.assertIsInstance(headerField.parameterNamesAndValueStrings, dict)
                self.assertEqual(301, headerField.integerValue)
                self.assertEqual(headerField.fieldName.lower(), self.canonicalCompactFieldNames[0].lower())
                self.assertEqual(headerField.fieldValueString, "301")
                self.assertEqual(self.canonicalCompactFieldNames[0] + ': 301', headerField.rawString)

