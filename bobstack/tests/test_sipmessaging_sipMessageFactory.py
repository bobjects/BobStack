try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from unittest import TestCase
import unittest
import sys
import settings
import subprocess
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
                self.appendStringToFileNamed(h + "\r\n", 'transactions')
                for startLine in l:
                    self.appendStringToFileNamed('    ' + startLine + "\r\n", 'transactions')
            for h, l in self.dialogHashesAndSIPMessages.iteritems():
                self.appendStringToFileNamed(h + "\r\n", 'dialogs')
                for startLine in l:
                    self.appendStringToFileNamed('    ' + startLine + "\r\n", 'dialogs')
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
            subprocess.call(['../../proprietary-test-data/analyzed/dedupelinefiles.sh'])
            print "finished de-duping."

    def printSIPMessageCounts(self):
        print "malformed: " + str(self.malformedSIPMessageCount)
        print "valid: " + str(self.validSIPMessageCount)
        print "invalid: " + str(self.invalidSIPMessageCount)
        print "valid known: " + str(self.validKnownSIPMessageCount)
        print "valid unknown: " + str(self.validUnknownSIPMessageCount)

    def handleMalformedSIPMessage(self, aSIPMessage):
        self.malformedSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'malformedSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'malformedSIPMessages')

    def handleValidSIPMessage(self, aSIPMessage):
        self.validSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'validSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPMessages')
        # print aSIPMessage.transactionHash
        # print aSIPMessage.dialogHash
        if aSIPMessage.transactionHash:
            if aSIPMessage.transactionHash not in self.transactionHashesAndSIPMessages:
                self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash] = []
            self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash].append(aSIPMessage.startLine.rawString)
        if aSIPMessage.dialogHash:
            if aSIPMessage.dialogHash not in self.dialogHashesAndSIPMessages:
                self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash] = []
            self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash].append(aSIPMessage.startLine.rawString)
        for headerField in aSIPMessage.header.headerFields:
            if headerField.isAccept:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'acceptHeaderFields')
            if headerField.isAcceptEncoding:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'acceptEncodingHeaderFields')
            if headerField.isAcceptLanguage:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'acceptLanguageHeaderFields')
            if headerField.isAllow:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'allowHeaderFields')
            if headerField.isAuthorization:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'authorizationHeaderFields')
            if headerField.isCallID:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'callIDHeaderFields')
            if headerField.isCallInfo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'callInfoHeaderFields')
            if headerField.isContact:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'contactHeaderFields')
            if headerField.isContentDisposition:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'contentDispositionHeaderFields')
            if headerField.isContentLength:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'contentLengthHeaderFields')
            if headerField.isContentType:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'contentTypeHeaderFields')
            if headerField.isCSeq:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'cSeqHeaderFields')
            if headerField.isDate:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'dateHeaderFields')
            if headerField.isExpires:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'expiresHeaderFields')
            if headerField.isFrom:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'fromHeaderFields')
            if headerField.isMaxForwards:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'maxForwardsHeaderFields')
            if headerField.isRecordRoute:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'recordRouteHeaderFields')
            if headerField.isRequire:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'requireHeaderFields')
            if headerField.isRetryAfter:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'retryAfterHeaderFields')
            if headerField.isRoute:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'routeHeaderFields')
            if headerField.isServer:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'serverHeaderFields')
            if headerField.isSessionExpires:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'sessionExpiresHeaderFields')
            if headerField.isSupported:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'supportedHeaderFields')
            if headerField.isTimestamp:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'timestampHeaderFields')
            if headerField.isTo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'toHeaderFields')
            if headerField.isUserAgent:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'userAgentHeaderFields')
            if headerField.isVia:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'viaHeaderFields')
            if headerField.isWarning:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'warningHeaderFields')
            if headerField.isWWWAuthenticate:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'wwwAuthenticateHeaderFields')
            if headerField.isVia:
                self.appendStringToFileNamed(headerField.rawString, 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    host:  ' + str(headerField.host), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    port:  ' + str(headerField.port), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    transport:  ' + str(headerField.transport), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    branch:  ' + str(headerField.branch), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(headerField.parameterNamesAndValueStrings), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed(str(headerField.branch), 'viaBranches')
                self.appendStringToFileNamed('\r\n', 'viaBranches')
            if headerField.isContact:
                self.appendStringToFileNamed(headerField.rawString, 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    displayName:  ' + str(headerField.displayName), 'contactHeaderFieldsAndAttributes')
                if headerField.sipURI:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(headerField.sipURI.scheme), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(headerField.sipURI.user), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(headerField.sipURI.host), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(headerField.sipURI.port), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(headerField.sipURI.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(headerField.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'contactHeaderFieldsAndAttributes')
            if headerField.isTo:
                self.appendStringToFileNamed(headerField.rawString, 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    displayName:  ' + str(headerField.displayName), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    tag:  ' + str(headerField.tag), 'toHeaderFieldsAndAttributes')
                if headerField.sipURI:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(headerField.sipURI.scheme), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(headerField.sipURI.user), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(headerField.sipURI.host), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(headerField.sipURI.port), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(headerField.sipURI.parameterNamesAndValueStrings), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(headerField.parameterNamesAndValueStrings), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'toHeaderFieldsAndAttributes')
                if headerField.tag:
                    self.appendStringToFileNamed(headerField.tag, 'toAndFromTags')
                    self.appendStringToFileNamed('\r\n', 'toAndFromTags')
            if headerField.isFrom:
                self.appendStringToFileNamed(headerField.rawString, 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    displayName:  ' + str(headerField.displayName), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    tag:  ' + str(headerField.tag), 'fromHeaderFieldsAndAttributes')
                if headerField.sipURI:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(headerField.sipURI.scheme), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(headerField.sipURI.user), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(headerField.sipURI.host), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(headerField.sipURI.port), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(headerField.sipURI.parameterNamesAndValueStrings), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(headerField.parameterNamesAndValueStrings), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'fromHeaderFieldsAndAttributes')
                if headerField.tag:
                    self.appendStringToFileNamed(headerField.tag, 'toAndFromTags')
                    self.appendStringToFileNamed('\r\n', 'toAndFromTags')
            if headerField.parameterNamesAndValueStrings:
                self.appendStringToFileNamed(headerField.rawString, 'headerFieldParameters')
                self.appendStringToFileNamed('\r\n', 'headerFieldParameters')
                for name, value in headerField.parameterNamesAndValueStrings.iteritems():
                    self.appendStringToFileNamed("    " + name + " : " + value + '\r\n', 'headerFieldParameters')
        for headerField in aSIPMessage.header.knownHeaderFields:
            self.appendStringToFileNamed(headerField.rawString, 'knownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFields')
        for headerField in aSIPMessage.header.knownHeaderFields:
            self.appendStringToFileNamed(headerField.fieldName, 'knownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFieldNames')
        for headerField in aSIPMessage.header.unknownHeaderFields:
            self.appendStringToFileNamed(headerField.rawString, 'unknownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFields')
        for headerField in aSIPMessage.header.unknownHeaderFields:
            self.appendStringToFileNamed(headerField.fieldName, 'unknownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFieldNames')

    def handleInvalidSIPMessage(self, aSIPMessage):
        self.invalidSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'invalidSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPMessages')
        for headerField in aSIPMessage.header.headerFields:
            if headerField.isInvalid:
                self.appendStringToFileNamed(headerField.rawString, 'invalidHeaderFields')

    def handleValidKnownSIPMessage(self, aSIPMessage):
        self.validKnownSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'validKnownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validKnownSIPMessages')
        if aSIPMessage.isRequest:
            self.appendStringToFileNamed(aSIPMessage.startLine.rawString, 'knownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'knownSIPStartLines')
            self.appendStringToFileNamed(aSIPMessage.startLine.sipMethod, 'knownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'knownSIPMethods')

    def handleValidUnknownSIPMessage(self, aSIPMessage):
        self.validUnknownSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'validUnknownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validUnknownSIPMessages')
        if aSIPMessage.isRequest:
            self.appendStringToFileNamed(aSIPMessage.startLine.rawString, 'unknownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'unknownSIPStartLines')
            self.appendStringToFileNamed(aSIPMessage.startLine.sipMethod, 'unknownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'unknownSIPMethods')

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
        self.assertIsInstance(aSIPMessage.isMalformed, bool)
        self.assertIsInstance(aSIPMessage.startLine.isMalformed, bool)
        self.assertIsInstance(aSIPMessage.startLine.isRequest, bool)
        self.assertIsInstance(aSIPMessage.startLine.isResponse, bool)
        self.assertIsInstance(aSIPMessage.content, basestring)
        # self.assertEqual(aSIPMessage.content__len__(), aSIPMessage.header.contentLength)
        # self.assertTrue(aSIPMessage.content__len__() in [aSIPMessage.header.contentLength, aSIPMessage.header.contentLength + 2)

    @property
    def sanitizedFilePathName(self):
        return '../../proprietary-test-data/sanitized/sanitized.txt'

    @property
    def messageSeparator(self):
        return "__MESSAGESEPARATOR__\r\n"

    def createFileNamed(self, fileName):
        self._fileNamesAndFiles[fileName] = open('../../proprietary-test-data/analyzed/' + fileName + ".txt", "w")

    def appendStringToFileNamed(self, aString, fileName):
        if fileName not in self._fileNamesAndFiles:
            self.createFileNamed(fileName)
        self._fileNamesAndFiles[fileName].write(aString)

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
