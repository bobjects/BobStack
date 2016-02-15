try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import unittest
import sys
import settings
#sys.path.append("..")
#from sipmessaging import SIPMessageFactory
sys.path.append("../..")
from abstractSIPRequestFromFactoryTestCase import AbstractSIPRequestFromFactoryTestCase
from abstractSIPResponseFromFactoryTestCase import AbstractSIPResponseFromFactoryTestCase
from abstractMalformedSIPMessageFromFactoryTestCase import AbstractMalformedSIPMessageFromFactoryTestCase
from bobstack.sipmessaging import SIPMessageFactory


class TestSIPMessageFactoryForSanitizedLogFile(TestCase):
    def setUp(self):
        self.malformedSIPMessageCount = 0
        self.validSIPMessageCount = 0
        self.invalidSIPMessageCount = 0
        self.validKnownSIPMessageCount = 0
        self.validUnknownSIPMessageCount = 0
        with open(self.malformedSIPMessagesPathName, "w"):
            pass
        with open(self.validSIPMessagesPathName, "w"):
            pass
        with open(self.invalidSIPMessagesPathName, "w"):
            pass
        with open(self.validKnownSIPMessagesPathName, "w"):
            pass
        with open(self.validUnknownSIPMessagesPathName, "w"):
            pass
        with open(self.knownSIPStartLinesPathName, "w"):
            pass
        with open(self.unknownSIPStartLinesPathName, "w"):
            pass
        with open(self.knownSIPMethodsPathName, "w"):
            pass
        with open(self.unknownSIPMethodsPathName, "w"):
            pass
        with open(self.knownHeaderFieldsPathName, "w"):
            pass
        with open(self.knownHeaderFieldNamesPathName, "w"):
            pass
        with open(self.unknownHeaderFieldsPathName, "w"):
            pass
        with open(self.unknownHeaderFieldNamesPathName, "w"):
            pass

    @unittest.skipIf(settings.skipLongTests, "Skipping long tests for now.")
    def test_parsing_sanitized_log_file(self):
        factory = SIPMessageFactory()
        factory.whenEventDo("malformedSIPMessage", self.handleMalformedSIPMessage)
        factory.whenEventDo("validSIPMessage", self.handleValidSIPMessage)
        factory.whenEventDo("invalidSIPMessage", self.handleInvalidSIPMessage)
        factory.whenEventDo("validKnownSIPMessage", self.handleValidKnownSIPMessage)
        factory.whenEventDo("validUnknownSIPMessage", self.handleValidUnknownSIPMessage)
        with open(self.sanitizedFilePathName, "r") as sanitizedFile:
            stringio = StringIO()
            count = 0
            for line in sanitizedFile:
                if line.startswith("__MESSAGESEPARATOR__"):
                    count += 1
                    messageString = stringio.getvalue()
                    self.assertTrue(messageString)

                    # with open("latesttestedmessage.txt", "w") as f:
                    #    f.write(messageString)
                    # pyperclip.copy(str(count) + "\n\n" + messageString)
                    if count % 5000 == 0:
                        print str(count)
                    sipMessage = factory.nextForString(messageString)
                    self.runAssertionsForSIPMessage(sipMessage)
                    stringio.close()
                    stringio = StringIO()
                else:
                    stringio.write(line)
        self.printSIPMessageCounts()

    def printSIPMessageCounts(self):
        print "malformed: " + str(self.malformedSIPMessageCount)
        print "valid: " + str(self.validSIPMessageCount)
        print "invalid: " + str(self.invalidSIPMessageCount)
        print "valid known: " + str(self.validKnownSIPMessageCount)
        print "valid unknown: " + str(self.validUnknownSIPMessageCount)

    def handleMalformedSIPMessage(self, aSIPMessage):
        self.malformedSIPMessageCount += 1
        with open(self.malformedSIPMessagesPathName, "a") as f:
            f.write(aSIPMessage.rawString)
            f.write(self.messageSeparator)

    def handleValidSIPMessage(self, aSIPMessage):
        self.validSIPMessageCount += 1
        with open(self.validSIPMessagesPathName, "a") as f:
            f.write(aSIPMessage.rawString)
            f.write(self.messageSeparator)
        with open(self.knownHeaderFieldsPathName, "a") as f:
            for headerField in aSIPMessage.header.knownHeaderFields:
                f.write(headerField.rawString)
                f.write("\r\n")
        with open(self.knownHeaderFieldNamesPathName, "a") as f:
            for headerField in aSIPMessage.header.knownHeaderFields:
                f.write(headerField.fieldName)
                f.write("\r\n")
        with open(self.unknownHeaderFieldsPathName, "a") as f:
            for headerField in aSIPMessage.header.unknownHeaderFields:
                f.write(headerField.rawString)
                f.write("\r\n")
        with open(self.unknownHeaderFieldNamesPathName, "a") as f:
            for headerField in aSIPMessage.header.unknownHeaderFields:
                f.write(headerField.fieldName)
                f.write("\r\n")

    def handleInvalidSIPMessage(self, aSIPMessage):
        self.invalidSIPMessageCount += 1
        with open(self.invalidSIPMessagesPathName, "a") as f:
            f.write(aSIPMessage.rawString)
            f.write(self.messageSeparator)

    def handleValidKnownSIPMessage(self, aSIPMessage):
        self.validKnownSIPMessageCount += 1
        with open(self.validKnownSIPMessagesPathName, "a") as f:
            f.write(aSIPMessage.rawString)
            f.write(self.messageSeparator)
        if aSIPMessage.isRequest:
            with open(self.knownSIPStartLinesPathName, "a") as f:
                f.write(aSIPMessage.startLine.rawString)
                f.write("\r\n")
            with open(self.knownSIPMethodsPathName, "a") as f:
                f.write(aSIPMessage.startLine.sipMethod)
                f.write("\r\n")
        # with open(self.knownHeaderFieldsPathName, "a") as f:
        #     for headerField in aSIPMessage.header.headerFields:
        #         f.write(headerField.rawString)
        #         f.write("\r\n")
        # with open(self.knownHeaderFieldNamesPathName, "a") as f:
        #     for headerField in aSIPMessage.header.headerFields:
        #         f.write(headerField.fieldName)
        #         f.write("\r\n")

    def handleValidUnknownSIPMessage(self, aSIPMessage):
        self.validUnknownSIPMessageCount += 1
        with open(self.validUnknownSIPMessagesPathName, "a") as f:
            f.write(aSIPMessage.rawString)
            f.write(self.messageSeparator)
        if aSIPMessage.isRequest:
            with open(self.unknownSIPStartLinesPathName, "a") as f:
                f.write(aSIPMessage.startLine.rawString)
                f.write("\r\n")
            with open(self.unknownSIPMethodsPathName, "a") as f:
                f.write(aSIPMessage.startLine.sipMethod)
                f.write("\r\n")
        # with open(self.unknownHeaderFieldsPathName, "a") as f:
        #     for headerField in aSIPMessage.header.headerFields:
        #         f.write(headerField.rawString)
        #         f.write("\r\n")
        # with open(self.unknownHeaderFieldNamesPathName, "a") as f:
        #     for headerField in aSIPMessage.header.headerFields:
        #         f.write(headerField.fieldName)
        #         f.write("\r\n")

    def runAssertionsForSIPMessage(self, aSIPMessage):
        self.assertTrue(aSIPMessage.rawString)
        self.assertIsInstance(aSIPMessage.isKnown, bool)
        self.assertIsInstance(aSIPMessage.isUnknown, bool)
        self.assertIsInstance(aSIPMessage.isValid, bool)
        self.assertIsInstance(aSIPMessage.isRequest, bool)
        self.assertIsInstance(aSIPMessage.isResponse, bool)
        self.assertIsInstance(aSIPMessage.isOPTIONSRequest, bool)
        self.assertIsInstance(aSIPMessage.isACKRequest, bool)
        self.assertIsInstance(aSIPMessage.isBYERequest, bool)
        self.assertIsInstance(aSIPMessage.isCANCELRequest, bool)
        self.assertIsInstance(aSIPMessage.isINFORequest, bool)
        self.assertIsInstance(aSIPMessage.isINVITERequest, bool)
        self.assertIsInstance(aSIPMessage.isNOTIFYRequest, bool)
        self.assertIsInstance(aSIPMessage.isREFERRequest, bool)
        self.assertIsInstance(aSIPMessage.isREGISTERRequest, bool)
        self.assertIsInstance(aSIPMessage.isSUBSCRIBERequest, bool)
        self.assertIsInstance(aSIPMessage.isUPDATERequest, bool)
        self.assertIsInstance(aSIPMessage.isMalformed, bool)
        # self.assertIsNotNone(aSIPMessage.header.contentLengthHeaderField)
        self.assertIsInstance(aSIPMessage.header.contentLength, (int, long))
        self.assertIsInstance(aSIPMessage.header.unknownHeaderFields, list)
        # print aSIPMessage.startLine.rawString
        # print aSIPMessage.rawString
        self.assertFalse(aSIPMessage.isMalformed)
        self.assertFalse(aSIPMessage.startLine.isMalformed)
        self.assertIsInstance(aSIPMessage.startLine.isRequest, bool)
        self.assertIsInstance(aSIPMessage.startLine.isResponse, bool)
        self.assertIsInstance(aSIPMessage.content, basestring)
        # self.assertEqual(aSIPMessage.content__len__(), aSIPMessage.header.contentLength)
        # self.assertTrue(aSIPMessage.content__len__() in [aSIPMessage.header.contentLength, aSIPMessage.header.contentLength + 2)

    @property
    def sanitizedFilePathName(self):
        return '../../proprietary-test-data/sanitized/sanitized.txt'

    @property
    def validSIPMessagesPathName(self):
        return '../../proprietary-test-data/sanitized/validSIPMessages.txt'

    @property
    def invalidSIPMessagesPathName(self):
        return '../../proprietary-test-data/sanitized/invalidSIPMessages.txt'

    @property
    def malformedSIPMessagesPathName(self):
        return '../../proprietary-test-data/sanitized/malformedSIPMessages.txt'

    @property
    def messageSeparator(self):
        return "__MESSAGESEPARATOR__\r\n"

    @property
    def validKnownSIPMessagesPathName(self):
        return '../../proprietary-test-data/sanitized/validKnownSIPMessages.txt'

    @property
    def validUnknownSIPMessagesPathName(self):
        return '../../proprietary-test-data/sanitized/validUnknownSIPMessages.txt'

    @property
    def knownSIPStartLinesPathName(self):
        return '../../proprietary-test-data/sanitized/knownSIPStartLines.txt'

    @property
    def unknownSIPStartLinesPathName(self):
        return '../../proprietary-test-data/sanitized/unknownSIPStartLines.txt'

    @property
    def knownSIPMethodsPathName(self):
        return '../../proprietary-test-data/sanitized/knownSIPMethods.txt'

    @property
    def unknownSIPMethodsPathName(self):
        return '../../proprietary-test-data/sanitized/unknownSIPMethods.txt'

    @property
    def knownHeaderFieldsPathName(self):
        return '../../proprietary-test-data/sanitized/knownHeaderFields.txt'

    @property
    def unknownHeaderFieldsPathName(self):
        return '../../proprietary-test-data/sanitized/unknownHeaderFields.txt'

    @property
    def knownHeaderFieldNamesPathName(self):
        return '../../proprietary-test-data/sanitized/knownHeaderFieldNames.txt'

    @property
    def unknownHeaderFieldNamesPathName(self):
        return '../../proprietary-test-data/sanitized/unknownHeaderFieldNames.txt'


class TestSIPMessageFactoryForMalformedSIPRequest(AbstractMalformedSIPMessageFromFactoryTestCase):
    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForMalformedSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForUnknownSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "UNKNOWN"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForUnknownSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForOPTIONSSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "OPTIONS"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForOPTIONSSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertTrue(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForACKSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "ACK"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForACKSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForBYESIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "BYE"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForBYESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertTrue(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForCANCELSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "CANCEL"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForCANCELSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertTrue(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForINFOSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "INFO"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForINFOSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertTrue(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForINVITESIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "INVITE"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForINVITESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertTrue(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForNOTIFYSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "NOTIFY"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForNOTIFYSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertTrue(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForREFERSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "REFER"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForREFERSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertTrue(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForREGISTERSIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "REGISTER"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForREGISTERSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertTrue(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForSUBSCRIBESIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "SUBSCRIBE"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForSUBSCRIBESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertTrue(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForUPDATESIPRequest(AbstractSIPRequestFromFactoryTestCase):
    @property
    def sipMethodString(self):
        return "UPDATE"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSIPMessageFactoryForUPDATESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertTrue(aSIPRequest.isUPDATERequest)


class TestSIPMessageFactoryForSIPResponse(AbstractSIPResponseFromFactoryTestCase):
    @property
    def statusCode(self):
        return 100

    @property
    def reasonPhrase(self):
        return "Trying"

    def test_parsing(self):
        self.run_test_parsing()

    def runAssertionsForSIPMessage(self, aSIPResponse):
        super(TestSIPMessageFactoryForSIPResponse, self).runAssertionsForSIPMessage(aSIPResponse)
        self.assertTrue(aSIPResponse.isKnown)
        self.assertFalse(aSIPResponse.isUnknown)
        self.assertFalse(aSIPResponse.isACKRequest)
        self.assertFalse(aSIPResponse.isBYERequest)
        self.assertFalse(aSIPResponse.isCANCELRequest)
        self.assertFalse(aSIPResponse.isINFORequest)
        self.assertFalse(aSIPResponse.isINVITERequest)
        self.assertFalse(aSIPResponse.isNOTIFYRequest)
        self.assertFalse(aSIPResponse.isOPTIONSRequest)
        self.assertFalse(aSIPResponse.isREFERRequest)
        self.assertFalse(aSIPResponse.isREGISTERRequest)
        self.assertFalse(aSIPResponse.isSUBSCRIBERequest)
        self.assertFalse(aSIPResponse.isUPDATERequest)
