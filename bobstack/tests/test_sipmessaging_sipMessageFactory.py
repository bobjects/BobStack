try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import unittest
import sys
import settings
import subprocess
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
        self.transactionHashesAndSIPMessages = {}
        self.dialogHashesAndSIPMessages = {}

    @unittest.skipIf(settings.skipLongTests, "Skipping long tests for now.")
    def test_parsing_sanitized_log_file(self):
        self._fileNamesAndFiles = {}
        # self.createFileNamed(self.malformedSIPMessagesPathName)
        # self.createFileNamed(self.validSIPMessagesPathName)
        # self.createFileNamed(self.invalidSIPMessagesPathName)
        # self.createFileNamed(self.validKnownSIPMessagesPathName)
        # self.createFileNamed(self.validUnknownSIPMessagesPathName)
        # self.createFileNamed(self.knownSIPStartLinesPathName)
        # self.createFileNamed(self.unknownSIPStartLinesPathName)
        # self.createFileNamed(self.knownSIPMethodsPathName)
        # self.createFileNamed(self.unknownSIPMethodsPathName)
        # self.createFileNamed(self.knownHeaderFieldsPathName)
        # self.createFileNamed(self.knownHeaderFieldNamesPathName)
        # self.createFileNamed(self.unknownHeaderFieldsPathName)
        # self.createFileNamed(self.unknownHeaderFieldNamesPathName)
        # self.createFileNamed(self.headerFieldParametersPathName)

        try:
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
                        if count % 5000 == 0:
                            print str(count)
                        sipMessage = factory.nextForString(messageString)
                        self.runAssertionsForSIPMessage(sipMessage)
                        stringio.close()
                        stringio = StringIO()
                    else:
                        stringio.write(line)
            self.printSIPMessageCounts()
        finally:
            for h, l in self.transactionHashesAndSIPMessages.iteritems():
                self.appendStringToFileNamed(h + "\r\n", self.transactionsPathName)
                for startLine in l:
                    self.appendStringToFileNamed('    ' + startLine + "\r\n", self.transactionsPathName)
            for h, l in self.dialogHashesAndSIPMessages.iteritems():
                self.appendStringToFileNamed(h + "\r\n", self.dialogsPathName)
                for startLine in l:
                    self.appendStringToFileNamed('    ' + startLine + "\r\n", self.dialogsPathName)
            self.closeFiles()
            # self.closeFileNamed(self.malformedSIPMessagesPathName)
            # self.closeFileNamed(self.validSIPMessagesPathName)
            # self.closeFileNamed(self.invalidSIPMessagesPathName)
            # self.closeFileNamed(self.validKnownSIPMessagesPathName)
            # self.closeFileNamed(self.validUnknownSIPMessagesPathName)
            # self.closeFileNamed(self.knownSIPStartLinesPathName)
            # self.closeFileNamed(self.unknownSIPStartLinesPathName)
            # self.closeFileNamed(self.knownSIPMethodsPathName)
            # self.closeFileNamed(self.unknownSIPMethodsPathName)
            # self.closeFileNamed(self.knownHeaderFieldsPathName)
            # self.closeFileNamed(self.knownHeaderFieldNamesPathName)
            # self.closeFileNamed(self.unknownHeaderFieldsPathName)
            # self.closeFileNamed(self.unknownHeaderFieldNamesPathName)
            # self.closeFileNamed(self.headerFieldParametersPathName)
            print "de-duping..."
            subprocess.call(['../../proprietary-test-data/sanitized/dedupelinefiles.sh'])
            print "finished de-duping."

    def printSIPMessageCounts(self):
        print "malformed: " + str(self.malformedSIPMessageCount)
        print "valid: " + str(self.validSIPMessageCount)
        print "invalid: " + str(self.invalidSIPMessageCount)
        print "valid known: " + str(self.validKnownSIPMessageCount)
        print "valid unknown: " + str(self.validUnknownSIPMessageCount)

    def handleMalformedSIPMessage(self, aSIPMessage):
        self.malformedSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, self.malformedSIPMessagesPathName)
        self.appendStringToFileNamed(self.messageSeparator, self.malformedSIPMessagesPathName)

    def handleValidSIPMessage(self, aSIPMessage):
        self.validSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, self.validSIPMessagesPathName)
        self.appendStringToFileNamed(self.messageSeparator, self.validSIPMessagesPathName)
        # print aSIPMessage.transactionHash
        # print aSIPMessage.dialogHash
        if aSIPMessage.transactionHash:
            if not aSIPMessage.transactionHash in self.transactionHashesAndSIPMessages:
                self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash] = []
            self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash].append(aSIPMessage.startLine.rawString)
        if aSIPMessage.dialogHash:
            if not aSIPMessage.dialogHash in self.dialogHashesAndSIPMessages:
                self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash] = []
            self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash].append(aSIPMessage.startLine.rawString)
        for headerField in aSIPMessage.header.headerFields:
            if headerField.isTo or headerField.isFrom:
                if headerField.tag:
                    self.appendStringToFileNamed(headerField.rawString, self.toAndFromTagsPathName)
                    self.appendStringToFileNamed('\r\n    ', self.toAndFromTagsPathName)
                    self.appendStringToFileNamed(headerField.tag, self.toAndFromTagsPathName)
                    self.appendStringToFileNamed('\r\n', self.toAndFromTagsPathName)
            if headerField.parameterNamesAndValues:
                self.appendStringToFileNamed(headerField.rawString, self.headerFieldParametersPathName)
                self.appendStringToFileNamed('\r\n', self.headerFieldParametersPathName)
                for name, value in headerField.parameterNamesAndValues.iteritems():
                    self.appendStringToFileNamed("    " + name + " : " + value + '\r\n', self.headerFieldParametersPathName)
        for headerField in aSIPMessage.header.knownHeaderFields:
            self.appendStringToFileNamed(headerField.rawString, self.knownHeaderFieldsPathName)
            self.appendStringToFileNamed("\r\n", self.knownHeaderFieldsPathName)
        for headerField in aSIPMessage.header.knownHeaderFields:
            self.appendStringToFileNamed(headerField.fieldName, self.knownHeaderFieldNamesPathName)
            self.appendStringToFileNamed("\r\n", self.knownHeaderFieldNamesPathName)
        for headerField in aSIPMessage.header.unknownHeaderFields:
            self.appendStringToFileNamed(headerField.rawString, self.unknownHeaderFieldsPathName)
            self.appendStringToFileNamed("\r\n", self.unknownHeaderFieldsPathName)
        for headerField in aSIPMessage.header.unknownHeaderFields:
            self.appendStringToFileNamed(headerField.fieldName, self.unknownHeaderFieldNamesPathName)
            self.appendStringToFileNamed("\r\n", self.unknownHeaderFieldNamesPathName)

    def handleInvalidSIPMessage(self, aSIPMessage):
        self.invalidSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, self.invalidSIPMessagesPathName)
        self.appendStringToFileNamed(self.messageSeparator, self.invalidSIPMessagesPathName)

    def handleValidKnownSIPMessage(self, aSIPMessage):
        self.validKnownSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, self.validKnownSIPMessagesPathName)
        self.appendStringToFileNamed(self.messageSeparator, self.validKnownSIPMessagesPathName)
        if aSIPMessage.isRequest:
            self.appendStringToFileNamed(aSIPMessage.startLine.rawString, self.knownSIPStartLinesPathName)
            self.appendStringToFileNamed("\r\n", self.knownSIPStartLinesPathName)
            self.appendStringToFileNamed(aSIPMessage.startLine.sipMethod, self.knownSIPMethodsPathName)
            self.appendStringToFileNamed("\r\n", self.knownSIPMethodsPathName)

    def handleValidUnknownSIPMessage(self, aSIPMessage):
        self.validUnknownSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, self.validUnknownSIPMessagesPathName)
        self.appendStringToFileNamed(self.messageSeparator, self.validUnknownSIPMessagesPathName)
        if aSIPMessage.isRequest:
            self.appendStringToFileNamed(aSIPMessage.startLine.rawString, self.unknownSIPStartLinesPathName)
            self.appendStringToFileNamed("\r\n", self.unknownSIPStartLinesPathName)
            self.appendStringToFileNamed(aSIPMessage.startLine.sipMethod, self.unknownSIPMethodsPathName)
            self.appendStringToFileNamed("\r\n", self.unknownSIPMethodsPathName)

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

    @property
    def headerFieldParametersPathName(self):
        return '../../proprietary-test-data/sanitized/headerFieldParameters.txt'

    @property
    def toAndFromTagsPathName(self):
        return '../../proprietary-test-data/sanitized/toAndFromTags.txt'

    @property
    def dialogsPathName(self):
        return '../../proprietary-test-data/sanitized/dialogs.txt'

    @property
    def transactionsPathName(self):
        return '../../proprietary-test-data/sanitized/transactions.txt'

    def createFileNamed(self, fileName):
        self._fileNamesAndFiles[fileName] = open(fileName, "w")
        # with open(fileName, "w"):
        #     pass

    def appendStringToFileNamed(self, aString, fileName):
        if fileName not in self._fileNamesAndFiles:
            self.createFileNamed(fileName)
        self._fileNamesAndFiles[fileName].write(aString)
        # with open(fileName, "a") as f:
        #     f.write(aString)

    def closeFiles(self):
        for fileName in self._fileNamesAndFiles.keys():
            self._fileNamesAndFiles[fileName].close()



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
