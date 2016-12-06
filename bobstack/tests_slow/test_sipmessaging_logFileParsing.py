try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import subprocess
import sys
import unittest
from unittest import TestCase

import testlogfilelocations

import settings

sys.path.append("../..")
sys.path.append("..")
from bobstack.sipmessaging import SIPMessageFactory
from sipmessaging import SIPURI


class TestSIPMessageFactoryForSanitizedLogFile(TestCase):
    def setUp(self):
        self.malformedSIPMessageCount = 0
        self.sipMessageCount = 0
        self.sipRequestCount = 0
        self.sipResponseCount = 0
        self.validSIPMessageCount = 0
        self.validSIPRequestCount = 0
        self.validSIPResponseCount = 0
        self.invalidSIPMessageCount = 0
        self.invalidSIPRequestCount = 0
        self.invalidSIPResponseCount = 0
        self.validKnownSIPMessageCount = 0
        self.validUnknownSIPMessageCount = 0
        self.transactionHashesAndSIPMessages = {}
        self.invariantBranchHashesAndSIPMessages = {}
        self.dialogHashesAndSIPMessages = {}

    # @unittest.skipIf(settings.skipLongTests, "Skipping long tests for now.\n")
    def test_parsing_sanitized_log_file(self):
        for sanitizedFilePathName, analyzedDirectoryPathName in self.sanitizedFileAndAnalyzedDirectoryPathName:
            self._analyzedDirectoryPathName = analyzedDirectoryPathName
            self._fileNamesAndFiles = {}
            try:
                factory = SIPMessageFactory()
                factory.whenEventDo("malformedSIPMessage", self.handleMalformedSIPMessage)
                factory.whenEventDo("sipMessage", self.handleSIPMessage)
                factory.whenEventDo("sipRequest", self.handleSIPRequest)
                factory.whenEventDo("sipResponse", self.handleSIPResponse)
                factory.whenEventDo("validSIPMessage", self.handleValidSIPMessage)
                factory.whenEventDo("validSIPRequest", self.handleValidSIPRequest)
                factory.whenEventDo("validSIPResponse", self.handleValidSIPResponse)
                factory.whenEventDo("invalidSIPMessage", self.handleInvalidSIPMessage)
                factory.whenEventDo("invalidSIPRequest", self.handleInvalidSIPRequest)
                factory.whenEventDo("invalidSIPResponse", self.handleInvalidSIPResponse)
                factory.whenEventDo("validKnownSIPMessage", self.handleValidKnownSIPMessage)
                factory.whenEventDo("validUnknownSIPMessage", self.handleValidUnknownSIPMessage)
                count = 0
                try:
                    with open(sanitizedFilePathName, "r") as sanitizedFile:
                        stringio = StringIO()
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
                except IOError:
                    pass
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
                for h, l in self.invariantBranchHashesAndSIPMessages.iteritems():
                    self.appendStringToFileNamed(h + "\r\n", 'invariantBranchHashes')
                    for startLine in l:
                        self.appendStringToFileNamed('    ' + startLine + "\r\n", 'invariantBranchHashes')
                self.closeFiles()
                if settings.writeAnalyzedFiles:
                    print "de-duping..."
                    try:
                        subprocess.call([self._analyzedDirectoryPathName + '/dedupelinefiles.sh'])
                    except OSError:
                        pass
                    print "finished de-duping."

    def printSIPMessageCounts(self):
        print "malformed: " + str(self.malformedSIPMessageCount)
        print "total messages: " + str(self.sipMessageCount)
        print "total requests: " + str(self.sipRequestCount)
        print "total responses: " + str(self.sipResponseCount)
        print "valid messages: " + str(self.validSIPMessageCount)
        print "valid requests: " + str(self.validSIPRequestCount)
        print "valid responses: " + str(self.validSIPResponseCount)
        print "invalid messages: " + str(self.invalidSIPMessageCount)
        print "invalid requests: " + str(self.invalidSIPRequestCount)
        print "invalid responses: " + str(self.invalidSIPResponseCount)
        print "valid known: " + str(self.validKnownSIPMessageCount)
        print "valid unknown: " + str(self.validUnknownSIPMessageCount)

        self.malformedSIPMessageCount = 0
        self.sipMessageCount = 0
        self.sipRequestCount = 0
        self.sipResponseCount = 0
        self.validSIPMessageCount = 0
        self.validSIPRequestCount = 0
        self.validSIPResponseCount = 0
        self.invalidSIPMessageCount = 0
        self.invalidSIPRequestCount = 0
        self.invalidSIPResponseCount = 0
        self.validKnownSIPMessageCount = 0
        self.validUnknownSIPMessageCount = 0

    def handleMalformedSIPMessage(self, aSIPMessage):
        self.malformedSIPMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'malformedSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'malformedSIPMessages')

    def handleValidSIPMessage(self, aSIPMessage):
        self.validSIPMessageCount += 1
        self.assertTrue(aSIPMessage.isValid)
        self.appendStringToFileNamed(aSIPMessage.rawString, 'validSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPMessages')
        # print aSIPMessage.transactionHash
        # print aSIPMessage.dialogHash
        if aSIPMessage.transactionHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if aSIPMessage.transactionHash not in self.transactionHashesAndSIPMessages:
            #     self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash] = []
            # self.transactionHashesAndSIPMessages[aSIPMessage.transactionHash].append(aSIPMessage.startLine.rawString)
        if aSIPMessage.header.invariantBranchHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if aSIPMessage.header.invariantBranchHash not in self.invariantBranchHashesAndSIPMessages:
            #     self.invariantBranchHashesAndSIPMessages[aSIPMessage.header.invariantBranchHash] = []
            # self.invariantBranchHashesAndSIPMessages[aSIPMessage.header.invariantBranchHash].append(aSIPMessage.startLine.rawString)
        if aSIPMessage.dialogHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if aSIPMessage.dialogHash not in self.dialogHashesAndSIPMessages:
            #     self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash] = []
            # self.dialogHashesAndSIPMessages[aSIPMessage.dialogHash].append(aSIPMessage.startLine.rawString)

        # TODO:  log these to files?
#        print aSIPMessage.rawString
#        print ""
        if aSIPMessage.header.callIDHeaderField:
            self.assertIsInstance(aSIPMessage.header.callID, basestring)
        else:
            self.assertIsInstance(aSIPMessage.header.callID, type(None))
        if aSIPMessage.header.cSeqHeaderField:
            self.assertIsInstance(aSIPMessage.header.cSeq, basestring)
        else:
            self.assertIsInstance(aSIPMessage.header.cSeq, type(None))
        self.assertIsInstance(aSIPMessage.header.toTag, (basestring, type(None)))
        self.assertIsInstance(aSIPMessage.header.fromTag, (basestring, type(None)))
        if aSIPMessage.header.maxForwardsHeaderField:
            self.assertIsInstance(aSIPMessage.header.maxForwards, int)
        else:
            self.assertIsInstance(aSIPMessage.header.maxForwards, type(None))
        self.assertIsInstance(aSIPMessage.header.routeURIs, list)
        self.assertIsInstance(aSIPMessage.header.recordRouteURIs, list)

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
            if headerField.isSubject:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'subjectSIPHeaderField')
            if headerField.isReferredBy:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'referredBySIPHeaderField')
            if headerField.isReferTo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'referToSIPHeaderField')
            if headerField.isAllowEvents:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'allowEventsSIPHeaderField')
            if headerField.isEvent:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'eventSIPHeaderField')
            if headerField.isContentEncoding:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'contentEncodingSIPHeaderField')
            if headerField.isRAck:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'rAckSIPHeaderField')
            if headerField.isPCharge:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'pChargeSIPHeaderField')
            if headerField.isReplyTo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'replyToSIPHeaderField')
            if headerField.isUnsupported:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'unsupportedSIPHeaderField')
            if headerField.isPAssertedIdentity:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'pAssertedIdentitySIPHeaderField')
            if headerField.isPPreferredIdentity:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'pPreferredIdentitySIPHeaderField')
            if headerField.isRemotePartyID:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'remotePartyIDSIPHeaderField')
            if headerField.isAlertInfo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'alertInfoSIPHeaderField')
            if headerField.isHistoryInfo:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'historyInfoSIPHeaderField')
            if headerField.isPCalledPartyId:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'pCalledPartyIdSIPHeaderField')
            if headerField.isPRTPStat:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'pRTPStatSIPHeaderField')
            if headerField.isPrivacy:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'privacySIPHeaderField')
            if headerField.isProxyAuthenticate:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'proxyAuthenticateSIPHeaderField')
            if headerField.isProxyAuthorization:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'proxyAuthorizationSIPHeaderField')
            if headerField.isProxyRequire:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'proxyRequireSIPHeaderField')
            if headerField.isReason:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'reasonSIPHeaderField')
            if headerField.isRecordSessionExpires:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'recordSessionExpiresSIPHeaderField')
            if headerField.isReplaces:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'replacesSIPHeaderField')
            if headerField.isSubscriptionState:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'subscriptionStateSIPHeaderField')
            if headerField.isMinExpires:
                self.appendStringToFileNamed(headerField.rawString + '\r\n', 'minExpiresSIPHeaderField')
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

    def handleValidSIPRequest(self, aSIPRequest):
        self.validSIPRequestCount += 1
        self.assertTrue(aSIPRequest.isRequest)
        self.assertTrue(aSIPRequest.isValid)
        self.appendStringToFileNamed(aSIPRequest.rawString, 'validSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPRequests')

    def handleValidSIPResponse(self, aSIPResponse):
        self.validSIPResponseCount += 1
        self.assertTrue(aSIPResponse.isResponse)
        self.assertTrue(aSIPResponse.isValid)
        self.appendStringToFileNamed(aSIPResponse.rawString, 'validSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPResponses')

    def handleInvalidSIPMessage(self, aSIPMessage):
        self.invalidSIPMessageCount += 1
        self.assertFalse(aSIPMessage.isValid)
        self.appendStringToFileNamed(aSIPMessage.rawString, 'invalidSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPMessages')
        for headerField in aSIPMessage.header.headerFields:
            if headerField.isInvalid:
                self.appendStringToFileNamed(headerField.rawString, 'invalidHeaderFields')

    def handleInvalidSIPRequest(self, aSIPRequest):
        self.invalidSIPRequestCount += 1
        self.assertTrue(aSIPRequest.isRequest)
        self.assertFalse(aSIPRequest.isValid)
        self.appendStringToFileNamed(aSIPRequest.rawString, 'invalidSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPRequests')

    def handleInvalidSIPResponse(self, aSIPResponse):
        self.invalidSIPResponseCount += 1
        self.assertTrue(aSIPResponse.isResponse)
        self.assertFalse(aSIPResponse.isValid)
        self.appendStringToFileNamed(aSIPResponse.rawString, 'invalidSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPResponses')

    def handleSIPMessage(self, aSIPMessage):
        self.sipMessageCount += 1
        self.appendStringToFileNamed(aSIPMessage.rawString, 'sipMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'sipMessages')

    def handleSIPRequest(self, aSIPRequest):
        self.sipRequestCount += 1
        self.assertTrue(aSIPRequest.isRequest)
        self.appendStringToFileNamed(aSIPRequest.rawString, 'sipRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'sipRequests')

    def handleSIPResponse(self, aSIPResponse):
        self.sipResponseCount += 1
        self.assertTrue(aSIPResponse.isResponse)
        self.appendStringToFileNamed(aSIPResponse.rawString, 'sipResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'sipResponses')

    def handleValidKnownSIPMessage(self, aSIPMessage):
        self.validKnownSIPMessageCount += 1
        self.assertTrue(aSIPMessage.isKnown)
        self.assertTrue(aSIPMessage.isValid)
        self.appendStringToFileNamed(aSIPMessage.rawString, 'validKnownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validKnownSIPMessages')
        if aSIPMessage.isRequest:
            self.appendStringToFileNamed(aSIPMessage.startLine.rawString, 'knownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'knownSIPStartLines')
            self.appendStringToFileNamed(aSIPMessage.startLine.sipMethod, 'knownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'knownSIPMethods')

    def handleValidUnknownSIPMessage(self, aSIPMessage):
        self.validUnknownSIPMessageCount += 1
        self.assertFalse(aSIPMessage.isKnown)
        self.assertTrue(aSIPMessage.isValid)
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
        self.assertIsInstance(aSIPMessage.isPRACKRequest, bool)
        self.assertIsInstance(aSIPMessage.isPUBLISHRequest, bool)
        self.assertIsInstance(aSIPMessage.isMESSAGERequest, bool)
        self.assertIsInstance(aSIPMessage.isREFERRequest, bool)
        self.assertIsInstance(aSIPMessage.isREGISTERRequest, bool)
        self.assertIsInstance(aSIPMessage.isSUBSCRIBERequest, bool)
        self.assertIsInstance(aSIPMessage.isUPDATERequest, bool)
        self.assertIsInstance(aSIPMessage.isMalformed, bool)
        # self.assertIsNotNone(aSIPMessage.header.contentLengthHeaderField)
        self.assertIsInstance(aSIPMessage.header.contentLength, (int, long))
        self.assertIsInstance(aSIPMessage.header.unknownHeaderFields, list)
        self.assertIsInstance(aSIPMessage.vias, list)
        self.assertIsInstance(aSIPMessage.header.vias, list)
        self.assertIsInstance(aSIPMessage.header.viaHeaderFields, list)
        self.assertIsInstance(aSIPMessage.routeURIs, list)
        self.assertIsInstance(aSIPMessage.header.routeURIs, list)
        self.assertIsInstance(aSIPMessage.header.routeHeaderFields, list)
        for u in aSIPMessage.routeURIs:
            self.assertIsInstance(u, SIPURI)
        self.assertIsInstance(aSIPMessage.recordRouteURIs, list)
        self.assertIsInstance(aSIPMessage.header.recordRouteURIs, list)
        self.assertIsInstance(aSIPMessage.header.recordRouteHeaderFields, list)
        for u in aSIPMessage.recordRouteURIs:
            self.assertIsInstance(u, SIPURI)
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
    def sanitizedFileAndAnalyzedDirectoryPathName(self):
        return [(dict['sanitizedFilePathName'], dict['analyzedDirectoryPathName']) for dict in testlogfilelocations.logFileDicts]

    @property
    def messageSeparator(self):
        return "__MESSAGESEPARATOR__\r\n"

    def createFileNamed(self, fileName):
        self._fileNamesAndFiles[fileName] = open(self._analyzedDirectoryPathName + '/' + fileName + ".txt", "w")

    def appendStringToFileNamed(self, aString, fileName):
        if settings.writeAnalyzedFiles:
            if fileName not in self._fileNamesAndFiles:
                self.createFileNamed(fileName)
            self._fileNamesAndFiles[fileName].write(aString)

    def closeFiles(self):
        for fileName in self._fileNamesAndFiles.keys():
            self._fileNamesAndFiles[fileName].close()