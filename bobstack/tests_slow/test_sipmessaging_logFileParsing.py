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
                                message_string = stringio.getvalue()
                                self.assertTrue(message_string)
                                if count % 5000 == 0:
                                    print str(count)
                                sipMessage = factory.nextForString(message_string)
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
                    for start_line in l:
                        self.appendStringToFileNamed('    ' + start_line + "\r\n", 'transactions')
                for h, l in self.dialogHashesAndSIPMessages.iteritems():
                    self.appendStringToFileNamed(h + "\r\n", 'dialogs')
                    for start_line in l:
                        self.appendStringToFileNamed('    ' + start_line + "\r\n", 'dialogs')
                for h, l in self.invariantBranchHashesAndSIPMessages.iteritems():
                    self.appendStringToFileNamed(h + "\r\n", 'invariantBranchHashes')
                    for start_line in l:
                        self.appendStringToFileNamed('    ' + start_line + "\r\n", 'invariantBranchHashes')
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

    def handleMalformedSIPMessage(self, a_sip_message):
        self.malformedSIPMessageCount += 1
        self.appendStringToFileNamed(a_sip_message.rawString, 'malformedSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'malformedSIPMessages')

    def handleValidSIPMessage(self, a_sip_message):
        self.validSIPMessageCount += 1
        self.assertTrue(a_sip_message.isValid)
        self.appendStringToFileNamed(a_sip_message.rawString, 'validSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPMessages')
        # print a_sip_message.transactionHash
        # print a_sip_message.dialogHash
        if a_sip_message.transactionHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.transactionHash not in self.transactionHashesAndSIPMessages:
            #     self.transactionHashesAndSIPMessages[a_sip_message.transactionHash] = []
            # self.transactionHashesAndSIPMessages[a_sip_message.transactionHash].append(a_sip_message.start_line.rawString)
        if a_sip_message.header.invariantBranchHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.header.invariantBranchHash not in self.invariantBranchHashesAndSIPMessages:
            #     self.invariantBranchHashesAndSIPMessages[a_sip_message.header.invariantBranchHash] = []
            # self.invariantBranchHashesAndSIPMessages[a_sip_message.header.invariantBranchHash].append(a_sip_message.start_line.rawString)
        if a_sip_message.dialogHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.dialogHash not in self.dialogHashesAndSIPMessages:
            #     self.dialogHashesAndSIPMessages[a_sip_message.dialogHash] = []
            # self.dialogHashesAndSIPMessages[a_sip_message.dialogHash].append(a_sip_message.start_line.rawString)

        # TODO:  log these to files?
#        print a_sip_message.rawString
#        print ""
        if a_sip_message.header.callIDHeaderField:
            self.assertIsInstance(a_sip_message.header.callID, basestring)
        else:
            self.assertIsInstance(a_sip_message.header.callID, type(None))
        if a_sip_message.header.cSeqHeaderField:
            self.assertIsInstance(a_sip_message.header.cSeq, basestring)
        else:
            self.assertIsInstance(a_sip_message.header.cSeq, type(None))
        self.assertIsInstance(a_sip_message.header.toTag, (basestring, type(None)))
        self.assertIsInstance(a_sip_message.header.fromTag, (basestring, type(None)))
        if a_sip_message.header.maxForwardsHeaderField:
            self.assertIsInstance(a_sip_message.header.maxForwards, int)
        else:
            self.assertIsInstance(a_sip_message.header.maxForwards, type(None))
        self.assertIsInstance(a_sip_message.header.routeURIs, list)
        self.assertIsInstance(a_sip_message.header.recordRouteURIs, list)

        for header_field in a_sip_message.header.header_fields:
            if header_field.isAccept:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'acceptHeaderFields')
            if header_field.isAcceptEncoding:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'acceptEncodingHeaderFields')
            if header_field.isAcceptLanguage:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'acceptLanguageHeaderFields')
            if header_field.isAllow:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'allowHeaderFields')
            if header_field.isAuthorization:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'authorizationHeaderFields')
            if header_field.isCallID:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'callIDHeaderFields')
            if header_field.isCallInfo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'callInfoHeaderFields')
            if header_field.isContact:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'contactHeaderFields')
            if header_field.isContentDisposition:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'contentDispositionHeaderFields')
            if header_field.isContentLength:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'contentLengthHeaderFields')
            if header_field.isContentType:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'contentTypeHeaderFields')
            if header_field.isCSeq:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'cSeqHeaderFields')
            if header_field.isDate:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'dateHeaderFields')
            if header_field.isExpires:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'expiresHeaderFields')
            if header_field.isFrom:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'fromHeaderFields')
            if header_field.isMaxForwards:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'maxForwardsHeaderFields')
            if header_field.isRecordRoute:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'recordRouteHeaderFields')
            if header_field.isRequire:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'requireHeaderFields')
            if header_field.isRetryAfter:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'retryAfterHeaderFields')
            if header_field.isRoute:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'routeHeaderFields')
            if header_field.isServer:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'serverHeaderFields')
            if header_field.isSessionExpires:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'sessionExpiresHeaderFields')
            if header_field.isSupported:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'supportedHeaderFields')
            if header_field.isTimestamp:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'timestampHeaderFields')
            if header_field.isTo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'toHeaderFields')
            if header_field.isUserAgent:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'userAgentHeaderFields')
            if header_field.isVia:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'viaHeaderFields')
            if header_field.isWarning:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'warningHeaderFields')
            if header_field.isWWWAuthenticate:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'wwwAuthenticateHeaderFields')
            if header_field.isSubject:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'subjectSIPHeaderField')
            if header_field.isReferredBy:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'referredBySIPHeaderField')
            if header_field.isReferTo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'referToSIPHeaderField')
            if header_field.isAllowEvents:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'allowEventsSIPHeaderField')
            if header_field.isEvent:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'eventSIPHeaderField')
            if header_field.isContentEncoding:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'contentEncodingSIPHeaderField')
            if header_field.isRAck:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'rAckSIPHeaderField')
            if header_field.isPCharge:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'pChargeSIPHeaderField')
            if header_field.isReplyTo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'replyToSIPHeaderField')
            if header_field.isUnsupported:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'unsupportedSIPHeaderField')
            if header_field.isPAssertedIdentity:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'pAssertedIdentitySIPHeaderField')
            if header_field.isPPreferredIdentity:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'pPreferredIdentitySIPHeaderField')
            if header_field.isRemotePartyID:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'remotePartyIDSIPHeaderField')
            if header_field.isAlertInfo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'alertInfoSIPHeaderField')
            if header_field.isHistoryInfo:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'historyInfoSIPHeaderField')
            if header_field.isPCalledPartyId:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'pCalledPartyIdSIPHeaderField')
            if header_field.isPRTPStat:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'pRTPStatSIPHeaderField')
            if header_field.isPrivacy:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'privacySIPHeaderField')
            if header_field.isProxyAuthenticate:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'proxyAuthenticateSIPHeaderField')
            if header_field.isProxyAuthorization:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'proxyAuthorizationSIPHeaderField')
            if header_field.isProxyRequire:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'proxyRequireSIPHeaderField')
            if header_field.isReason:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'reasonSIPHeaderField')
            if header_field.isRecordSessionExpires:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'recordSessionExpiresSIPHeaderField')
            if header_field.isReplaces:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'replacesSIPHeaderField')
            if header_field.isSubscriptionState:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'subscriptionStateSIPHeaderField')
            if header_field.isMinExpires:
                self.appendStringToFileNamed(header_field.rawString + '\r\n', 'minExpiresSIPHeaderField')
            if header_field.isVia:
                self.appendStringToFileNamed(header_field.rawString, 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    host:  ' + str(header_field.host), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    port:  ' + str(header_field.port), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    transport:  ' + str(header_field.transport), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    branch:  ' + str(header_field.branch), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed(str(header_field.branch), 'viaBranches')
                self.appendStringToFileNamed('\r\n', 'viaBranches')
            if header_field.isContact:
                self.appendStringToFileNamed(header_field.rawString, 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    display_name:  ' + str(header_field.display_name), 'contactHeaderFieldsAndAttributes')
                if header_field.sip_uri:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(header_field.sip_uri.scheme), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(header_field.sip_uri.user), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(header_field.sip_uri.host), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(header_field.sip_uri.port), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(header_field.sip_uri.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'contactHeaderFieldsAndAttributes')
            if header_field.isTo:
                self.appendStringToFileNamed(header_field.rawString, 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    display_name:  ' + str(header_field.display_name), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    tag:  ' + str(header_field.tag), 'toHeaderFieldsAndAttributes')
                if header_field.sip_uri:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(header_field.sip_uri.scheme), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(header_field.sip_uri.user), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(header_field.sip_uri.host), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(header_field.sip_uri.port), 'toHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(header_field.sip_uri.parameterNamesAndValueStrings), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'toHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'toHeaderFieldsAndAttributes')
                if header_field.tag:
                    self.appendStringToFileNamed(header_field.tag, 'toAndFromTags')
                    self.appendStringToFileNamed('\r\n', 'toAndFromTags')
            if header_field.isFrom:
                self.appendStringToFileNamed(header_field.rawString, 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    display_name:  ' + str(header_field.display_name), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    tag:  ' + str(header_field.tag), 'fromHeaderFieldsAndAttributes')
                if header_field.sip_uri:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(header_field.sip_uri.scheme), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(header_field.sip_uri.user), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(header_field.sip_uri.host), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(header_field.sip_uri.port), 'fromHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(header_field.sip_uri.parameterNamesAndValueStrings), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'fromHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'fromHeaderFieldsAndAttributes')
                if header_field.tag:
                    self.appendStringToFileNamed(header_field.tag, 'toAndFromTags')
                    self.appendStringToFileNamed('\r\n', 'toAndFromTags')
            if header_field.parameterNamesAndValueStrings:
                self.appendStringToFileNamed(header_field.rawString, 'headerFieldParameters')
                self.appendStringToFileNamed('\r\n', 'headerFieldParameters')
                for name, value in header_field.parameterNamesAndValueStrings.iteritems():
                    self.appendStringToFileNamed("    " + name + " : " + value + '\r\n', 'headerFieldParameters')
        for header_field in a_sip_message.header.knownHeaderFields:
            self.appendStringToFileNamed(header_field.rawString, 'knownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFields')
        for header_field in a_sip_message.header.knownHeaderFields:
            self.appendStringToFileNamed(header_field.field_name, 'knownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFieldNames')
        for header_field in a_sip_message.header.unknownHeaderFields:
            self.appendStringToFileNamed(header_field.rawString, 'unknownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFields')
        for header_field in a_sip_message.header.unknownHeaderFields:
            self.appendStringToFileNamed(header_field.field_name, 'unknownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFieldNames')

    def handleValidSIPRequest(self, a_sip_request):
        self.validSIPRequestCount += 1
        self.assertTrue(a_sip_request.isRequest)
        self.assertTrue(a_sip_request.isValid)
        self.appendStringToFileNamed(a_sip_request.rawString, 'validSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPRequests')

    def handleValidSIPResponse(self, a_sip_response):
        self.validSIPResponseCount += 1
        self.assertTrue(a_sip_response.isResponse)
        self.assertTrue(a_sip_response.isValid)
        self.appendStringToFileNamed(a_sip_response.rawString, 'validSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPResponses')

    def handleInvalidSIPMessage(self, a_sip_message):
        self.invalidSIPMessageCount += 1
        self.assertFalse(a_sip_message.isValid)
        self.appendStringToFileNamed(a_sip_message.rawString, 'invalidSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPMessages')
        for header_field in a_sip_message.header.header_fields:
            if header_field.isInvalid:
                self.appendStringToFileNamed(header_field.rawString, 'invalidHeaderFields')

    def handleInvalidSIPRequest(self, a_sip_request):
        self.invalidSIPRequestCount += 1
        self.assertTrue(a_sip_request.isRequest)
        self.assertFalse(a_sip_request.isValid)
        self.appendStringToFileNamed(a_sip_request.rawString, 'invalidSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPRequests')

    def handleInvalidSIPResponse(self, a_sip_response):
        self.invalidSIPResponseCount += 1
        self.assertTrue(a_sip_response.isResponse)
        self.assertFalse(a_sip_response.isValid)
        self.appendStringToFileNamed(a_sip_response.rawString, 'invalidSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPResponses')

    def handleSIPMessage(self, a_sip_message):
        self.sipMessageCount += 1
        self.appendStringToFileNamed(a_sip_message.rawString, 'sipMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'sipMessages')

    def handleSIPRequest(self, a_sip_request):
        self.sipRequestCount += 1
        self.assertTrue(a_sip_request.isRequest)
        self.appendStringToFileNamed(a_sip_request.rawString, 'sipRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'sipRequests')

    def handleSIPResponse(self, a_sip_response):
        self.sipResponseCount += 1
        self.assertTrue(a_sip_response.isResponse)
        self.appendStringToFileNamed(a_sip_response.rawString, 'sipResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'sipResponses')

    def handleValidKnownSIPMessage(self, a_sip_message):
        self.validKnownSIPMessageCount += 1
        self.assertTrue(a_sip_message.isKnown)
        self.assertTrue(a_sip_message.isValid)
        self.appendStringToFileNamed(a_sip_message.rawString, 'validKnownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validKnownSIPMessages')
        if a_sip_message.isRequest:
            self.appendStringToFileNamed(a_sip_message.start_line.rawString, 'knownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'knownSIPStartLines')
            self.appendStringToFileNamed(a_sip_message.start_line.sip_method, 'knownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'knownSIPMethods')

    def handleValidUnknownSIPMessage(self, a_sip_message):
        self.validUnknownSIPMessageCount += 1
        self.assertFalse(a_sip_message.isKnown)
        self.assertTrue(a_sip_message.isValid)
        self.appendStringToFileNamed(a_sip_message.rawString, 'validUnknownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validUnknownSIPMessages')
        if a_sip_message.isRequest:
            self.appendStringToFileNamed(a_sip_message.start_line.rawString, 'unknownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'unknownSIPStartLines')
            self.appendStringToFileNamed(a_sip_message.start_line.sip_method, 'unknownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'unknownSIPMethods')

    def runAssertionsForSIPMessage(self, a_sip_message):
        self.assertTrue(a_sip_message.rawString)
        self.assertIsInstance(a_sip_message.isKnown, bool)
        self.assertIsInstance(a_sip_message.isUnknown, bool)
        self.assertIsInstance(a_sip_message.isValid, bool)
        self.assertIsInstance(a_sip_message.isRequest, bool)
        self.assertIsInstance(a_sip_message.isResponse, bool)
        self.assertIsInstance(a_sip_message.isOPTIONSRequest, bool)
        self.assertIsInstance(a_sip_message.isACKRequest, bool)
        self.assertIsInstance(a_sip_message.isBYERequest, bool)
        self.assertIsInstance(a_sip_message.isCANCELRequest, bool)
        self.assertIsInstance(a_sip_message.isINFORequest, bool)
        self.assertIsInstance(a_sip_message.isINVITERequest, bool)
        self.assertIsInstance(a_sip_message.isNOTIFYRequest, bool)
        self.assertIsInstance(a_sip_message.isPRACKRequest, bool)
        self.assertIsInstance(a_sip_message.isPUBLISHRequest, bool)
        self.assertIsInstance(a_sip_message.isMESSAGERequest, bool)
        self.assertIsInstance(a_sip_message.isREFERRequest, bool)
        self.assertIsInstance(a_sip_message.isREGISTERRequest, bool)
        self.assertIsInstance(a_sip_message.isSUBSCRIBERequest, bool)
        self.assertIsInstance(a_sip_message.isUPDATERequest, bool)
        self.assertIsInstance(a_sip_message.isMalformed, bool)
        # self.assertIsNotNone(a_sip_message.header.contentLengthHeaderField)
        self.assertIsInstance(a_sip_message.header.contentLength, (int, long))
        self.assertIsInstance(a_sip_message.header.unknownHeaderFields, list)
        self.assertIsInstance(a_sip_message.vias, list)
        self.assertIsInstance(a_sip_message.header.vias, list)
        self.assertIsInstance(a_sip_message.header.viaHeaderFields, list)
        self.assertIsInstance(a_sip_message.routeURIs, list)
        self.assertIsInstance(a_sip_message.header.routeURIs, list)
        self.assertIsInstance(a_sip_message.header.routeHeaderFields, list)
        for u in a_sip_message.routeURIs:
            self.assertIsInstance(u, SIPURI)
        self.assertIsInstance(a_sip_message.recordRouteURIs, list)
        self.assertIsInstance(a_sip_message.header.recordRouteURIs, list)
        self.assertIsInstance(a_sip_message.header.recordRouteHeaderFields, list)
        for u in a_sip_message.recordRouteURIs:
            self.assertIsInstance(u, SIPURI)
        # print a_sip_message.start_line.rawString
        # print a_sip_message.rawString
        self.assertIsInstance(a_sip_message.isMalformed, bool)
        self.assertIsInstance(a_sip_message.start_line.isMalformed, bool)
        self.assertIsInstance(a_sip_message.start_line.isRequest, bool)
        self.assertIsInstance(a_sip_message.start_line.isResponse, bool)
        self.assertIsInstance(a_sip_message.content, basestring)
        # self.assertEqual(a_sip_message.content__len__(), a_sip_message.header.contentLength)
        # self.assertTrue(a_sip_message.content__len__() in [a_sip_message.header.contentLength, a_sip_message.header.contentLength + 2)

    @property
    def sanitizedFileAndAnalyzedDirectoryPathName(self):
        return [(dict['sanitizedFilePathName'], dict['analyzedDirectoryPathName']) for dict in testlogfilelocations.logFileDicts]

    @property
    def messageSeparator(self):
        return "__MESSAGESEPARATOR__\r\n"

    def createFileNamed(self, file_name):
        self._fileNamesAndFiles[file_name] = open(self._analyzedDirectoryPathName + '/' + file_name + ".txt", "w")

    def appendStringToFileNamed(self, a_string, file_name):
        if settings.writeAnalyzedFiles:
            if file_name not in self._fileNamesAndFiles:
                self.createFileNamed(file_name)
            self._fileNamesAndFiles[file_name].write(a_string)

    def closeFiles(self):
        for file_name in self._fileNamesAndFiles.keys():
            self._fileNamesAndFiles[file_name].close()
