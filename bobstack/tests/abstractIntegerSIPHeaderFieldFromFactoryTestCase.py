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
from abstractSIPHeaderFieldFromFactoryTestCase import AbstractSIPHeaderFieldFromFactoryTestCase



class AbstractIntegerSIPHeaderFieldFromFactoryTestCase(AbstractSIPHeaderFieldFromFactoryTestCase):
    @property
    def canonicalFieldValues(self):
        return ["489"]

    def basic_test_parsing(self):
        super(AbstractIntegerSIPHeaderFieldFromFactoryTestCase, self).basic_test_parsing()
        for line in self.canonicalStrings:
            headerField = SIPHeaderFieldFactory().nextForString(line)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertIsInstance(headerField.value, (int, long), line)
            self.assertEqual(headerField.value, int(self.canonicalFieldValues[0]))
            headerField.rawString = self.canonicalFieldNames[0] + ': 301'
            self.assertEqual(301, headerField.value)
            self.assertEqual(headerField.fieldName.lower(), self.canonicalFieldNames[0].lower())
            self.assertEqual(headerField.fieldValue, "301")
            self.assertEqual(self.canonicalFieldNames[0] + ': 301', headerField.rawString)
