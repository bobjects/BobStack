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
                factory.when_event_do("malformedSIPMessage", self.handleMalformedSIPMessage)
                factory.when_event_do("sipMessage", self.handleSIPMessage)
                factory.when_event_do("sipRequest", self.handleSIPRequest)
                factory.when_event_do("sipResponse", self.handleSIPResponse)
                factory.when_event_do("validSIPMessage", self.handleValidSIPMessage)
                factory.when_event_do("validSIPRequest", self.handleValidSIPRequest)
                factory.when_event_do("validSIPResponse", self.handleValidSIPResponse)
                factory.when_event_do("invalidSIPMessage", self.handleInvalidSIPMessage)
                factory.when_event_do("invalidSIPRequest", self.handleInvalidSIPRequest)
                factory.when_event_do("invalidSIPResponse", self.handleInvalidSIPResponse)
                factory.when_event_do("validKnownSIPMessage", self.handleValidKnownSIPMessage)
                factory.when_event_do("validUnknownSIPMessage", self.handleValidUnknownSIPMessage)
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
                                    print(str(count))
                                sip_message = factory.next_for_string(message_string)
                                self.runAssertionsForSIPMessage(sip_message)
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
                    print("de-duping...")
                    try:
                        subprocess.call([self._analyzedDirectoryPathName + '/dedupelinefiles.sh'])
                    except OSError:
                        pass
                    print("finished de-duping.")

    def printSIPMessageCounts(self):
        print("malformed: " + str(self.malformedSIPMessageCount))
        print("total messages: " + str(self.sipMessageCount))
        print("total requests: " + str(self.sipRequestCount))
        print("total responses: " + str(self.sipResponseCount))
        print("valid messages: " + str(self.validSIPMessageCount))
        print("valid requests: " + str(self.validSIPRequestCount))
        print("valid responses: " + str(self.validSIPResponseCount))
        print("invalid messages: " + str(self.invalidSIPMessageCount))
        print("invalid requests: " + str(self.invalidSIPRequestCount))
        print("invalid responses: " + str(self.invalidSIPResponseCount))
        print("valid known: " + str(self.validKnownSIPMessageCount))
        print("valid unknown: " + str(self.validUnknownSIPMessageCount))

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
        self.appendStringToFileNamed(a_sip_message.raw_string, 'malformedSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'malformedSIPMessages')

    def handleValidSIPMessage(self, a_sip_message):
        self.validSIPMessageCount += 1
        self.assertTrue(a_sip_message.is_valid)
        self.appendStringToFileNamed(a_sip_message.raw_string, 'validSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPMessages')
        # print a_sip_message.transactionHash
        # print a_sip_message.dialogHash
        if a_sip_message.transactionHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.transactionHash not in self.transactionHashesAndSIPMessages:
            #     self.transactionHashesAndSIPMessages[a_sip_message.transactionHash] = []
            # self.transactionHashesAndSIPMessages[a_sip_message.transactionHash].append(a_sip_message.start_line.raw_string)
        if a_sip_message.header.invariantBranchHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.header.invariantBranchHash not in self.invariantBranchHashesAndSIPMessages:
            #     self.invariantBranchHashesAndSIPMessages[a_sip_message.header.invariantBranchHash] = []
            # self.invariantBranchHashesAndSIPMessages[a_sip_message.header.invariantBranchHash].append(a_sip_message.start_line.raw_string)
        if a_sip_message.dialogHash:
            pass
            # TODO:  running into memory issues on small VMs.  Are these dicts the culprit?
            # if a_sip_message.dialogHash not in self.dialogHashesAndSIPMessages:
            #     self.dialogHashesAndSIPMessages[a_sip_message.dialogHash] = []
            # self.dialogHashesAndSIPMessages[a_sip_message.dialogHash].append(a_sip_message.start_line.raw_string)

        # TODO:  log these to files?
#        print a_sip_message.raw_string
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
            self.assertIsInstance(a_sip_message.header.max_forwards, int)
        else:
            self.assertIsInstance(a_sip_message.header.max_forwards, type(None))
        self.assertIsInstance(a_sip_message.header.routeURIs, list)
        self.assertIsInstance(a_sip_message.header.recordRouteURIs, list)

        for header_field in a_sip_message.header.header_fields:
            if header_field.is_accept:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'acceptHeaderFields')
            if header_field.is_accept_encoding:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'acceptEncodingHeaderFields')
            if header_field.is_accept_language:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'acceptLanguageHeaderFields')
            if header_field.is_allow:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'allowHeaderFields')
            if header_field.is_authorization:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'authorizationHeaderFields')
            if header_field.is_call_id:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'callIDHeaderFields')
            if header_field.is_call_info:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'callInfoHeaderFields')
            if header_field.is_contact:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'contactHeaderFields')
            if header_field.is_content_disposition:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'contentDispositionHeaderFields')
            if header_field.is_content_length:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'contentLengthHeaderFields')
            if header_field.is_content_type:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'contentTypeHeaderFields')
            if header_field.is_cseq:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'cSeqHeaderFields')
            if header_field.is_date:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'dateHeaderFields')
            if header_field.is_expires:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'expiresHeaderFields')
            if header_field.is_from:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'fromHeaderFields')
            if header_field.is_max_forwards:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'maxForwardsHeaderFields')
            if header_field.is_record_route:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'recordRouteHeaderFields')
            if header_field.is_require:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'requireHeaderFields')
            if header_field.is_retry_after:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'retryAfterHeaderFields')
            if header_field.is_route:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'routeHeaderFields')
            if header_field.is_server:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'serverHeaderFields')
            if header_field.is_session_expires:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'sessionExpiresHeaderFields')
            if header_field.is_supported:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'supportedHeaderFields')
            if header_field.is_timestamp:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'timestampHeaderFields')
            if header_field.is_to:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'toHeaderFields')
            if header_field.is_user_agent:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'userAgentHeaderFields')
            if header_field.is_via:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'viaHeaderFields')
            if header_field.is_warning:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'warningHeaderFields')
            if header_field.is_www_authenticate:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'wwwAuthenticateHeaderFields')
            if header_field.is_subject:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'subjectSIPHeaderField')
            if header_field.is_referred_by:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'referredBySIPHeaderField')
            if header_field.is_refer_to:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'referToSIPHeaderField')
            if header_field.is_allow_events:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'allowEventsSIPHeaderField')
            if header_field.is_event:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'eventSIPHeaderField')
            if header_field.is_content_encoding:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'contentEncodingSIPHeaderField')
            if header_field.is_rack:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'rAckSIPHeaderField')
            if header_field.is_p_charge:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'pChargeSIPHeaderField')
            if header_field.is_reply_to:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'replyToSIPHeaderField')
            if header_field.is_unsupported:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'unsupportedSIPHeaderField')
            if header_field.is_p_asserted_identity:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'pAssertedIdentitySIPHeaderField')
            if header_field.is_p_preferred_identity:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'pPreferredIdentitySIPHeaderField')
            if header_field.is_remote_party_id:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'remotePartyIDSIPHeaderField')
            if header_field.is_alert_info:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'alertInfoSIPHeaderField')
            if header_field.is_history_info:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'historyInfoSIPHeaderField')
            if header_field.is_p_called_party_id:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'pCalledPartyIdSIPHeaderField')
            if header_field.is_p_rtp_stat:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'pRTPStatSIPHeaderField')
            if header_field.is_privacy:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'privacySIPHeaderField')
            if header_field.is_proxy_authenticate:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'proxyAuthenticateSIPHeaderField')
            if header_field.is_proxy_authorization:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'proxyAuthorizationSIPHeaderField')
            if header_field.is_proxy_require:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'proxyRequireSIPHeaderField')
            if header_field.is_reason:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'reasonSIPHeaderField')
            if header_field.is_record_session_expires:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'recordSessionExpiresSIPHeaderField')
            if header_field.is_replaces:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'replacesSIPHeaderField')
            if header_field.is_subscription_state:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'subscriptionStateSIPHeaderField')
            if header_field.is_min_expires:
                self.appendStringToFileNamed(header_field.raw_string + '\r\n', 'minExpiresSIPHeaderField')
            if header_field.is_via:
                self.appendStringToFileNamed(header_field.raw_string, 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    host:  ' + str(header_field.host), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    port:  ' + str(header_field.port), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    transport:  ' + str(header_field.transport), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    branch:  ' + str(header_field.branch), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'viaHeaderFieldsAndAttributes')
                self.appendStringToFileNamed(str(header_field.branch), 'viaBranches')
                self.appendStringToFileNamed('\r\n', 'viaBranches')
            if header_field.is_contact:
                self.appendStringToFileNamed(header_field.raw_string, 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    display_name:  ' + str(header_field.display_name), 'contactHeaderFieldsAndAttributes')
                if header_field.sip_uri:
                    self.appendStringToFileNamed('\r\n        scheme:  ' + str(header_field.sip_uri.scheme), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        user:  ' + str(header_field.sip_uri.user), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        host:  ' + str(header_field.sip_uri.host), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        port:  ' + str(header_field.sip_uri.port), 'contactHeaderFieldsAndAttributes')
                    self.appendStringToFileNamed('\r\n        uriParameters:  ' + str(header_field.sip_uri.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n    headerFieldParameters:  ' + str(header_field.parameterNamesAndValueStrings), 'contactHeaderFieldsAndAttributes')
                self.appendStringToFileNamed('\r\n', 'contactHeaderFieldsAndAttributes')
            if header_field.is_to:
                self.appendStringToFileNamed(header_field.raw_string, 'toHeaderFieldsAndAttributes')
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
            if header_field.is_from:
                self.appendStringToFileNamed(header_field.raw_string, 'fromHeaderFieldsAndAttributes')
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
                self.appendStringToFileNamed(header_field.raw_string, 'headerFieldParameters')
                self.appendStringToFileNamed('\r\n', 'headerFieldParameters')
                for name, value in header_field.parameterNamesAndValueStrings.iteritems():
                    self.appendStringToFileNamed("    " + name + " : " + value + '\r\n', 'headerFieldParameters')
        for header_field in a_sip_message.header.knownHeaderFields:
            self.appendStringToFileNamed(header_field.raw_string, 'knownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFields')
        for header_field in a_sip_message.header.knownHeaderFields:
            self.appendStringToFileNamed(header_field.field_name, 'knownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'knownHeaderFieldNames')
        for header_field in a_sip_message.header.unknownHeaderFields:
            self.appendStringToFileNamed(header_field.raw_string, 'unknownHeaderFields')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFields')
        for header_field in a_sip_message.header.unknownHeaderFields:
            self.appendStringToFileNamed(header_field.field_name, 'unknownHeaderFieldNames')
            self.appendStringToFileNamed("\r\n", 'unknownHeaderFieldNames')

    def handleValidSIPRequest(self, a_sip_request):
        self.validSIPRequestCount += 1
        self.assertTrue(a_sip_request.is_request)
        self.assertTrue(a_sip_request.is_valid)
        self.appendStringToFileNamed(a_sip_request.raw_string, 'validSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPRequests')

    def handleValidSIPResponse(self, a_sip_response):
        self.validSIPResponseCount += 1
        self.assertTrue(a_sip_response.is_response)
        self.assertTrue(a_sip_response.is_valid)
        self.appendStringToFileNamed(a_sip_response.raw_string, 'validSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'validSIPResponses')

    def handleInvalidSIPMessage(self, a_sip_message):
        self.invalidSIPMessageCount += 1
        self.assertFalse(a_sip_message.is_valid)
        self.appendStringToFileNamed(a_sip_message.raw_string, 'invalidSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPMessages')
        for header_field in a_sip_message.header.header_fields:
            if header_field.isInvalid:
                self.appendStringToFileNamed(header_field.raw_string, 'invalidHeaderFields')

    def handleInvalidSIPRequest(self, a_sip_request):
        self.invalidSIPRequestCount += 1
        self.assertTrue(a_sip_request.is_request)
        self.assertFalse(a_sip_request.is_valid)
        self.appendStringToFileNamed(a_sip_request.raw_string, 'invalidSIPRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPRequests')

    def handleInvalidSIPResponse(self, a_sip_response):
        self.invalidSIPResponseCount += 1
        self.assertTrue(a_sip_response.is_response)
        self.assertFalse(a_sip_response.is_valid)
        self.appendStringToFileNamed(a_sip_response.raw_string, 'invalidSIPResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'invalidSIPResponses')

    def handleSIPMessage(self, a_sip_message):
        self.sipMessageCount += 1
        self.appendStringToFileNamed(a_sip_message.raw_string, 'sipMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'sipMessages')

    def handleSIPRequest(self, a_sip_request):
        self.sipRequestCount += 1
        self.assertTrue(a_sip_request.is_request)
        self.appendStringToFileNamed(a_sip_request.raw_string, 'sipRequests')
        self.appendStringToFileNamed(self.messageSeparator, 'sipRequests')

    def handleSIPResponse(self, a_sip_response):
        self.sipResponseCount += 1
        self.assertTrue(a_sip_response.is_response)
        self.appendStringToFileNamed(a_sip_response.raw_string, 'sipResponses')
        self.appendStringToFileNamed(self.messageSeparator, 'sipResponses')

    def handleValidKnownSIPMessage(self, a_sip_message):
        self.validKnownSIPMessageCount += 1
        self.assertTrue(a_sip_message.is_known)
        self.assertTrue(a_sip_message.is_valid)
        self.appendStringToFileNamed(a_sip_message.raw_string, 'validKnownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validKnownSIPMessages')
        if a_sip_message.is_request:
            self.appendStringToFileNamed(a_sip_message.start_line.raw_string, 'knownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'knownSIPStartLines')
            self.appendStringToFileNamed(a_sip_message.start_line.sip_method, 'knownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'knownSIPMethods')

    def handleValidUnknownSIPMessage(self, a_sip_message):
        self.validUnknownSIPMessageCount += 1
        self.assertFalse(a_sip_message.is_known)
        self.assertTrue(a_sip_message.is_valid)
        self.appendStringToFileNamed(a_sip_message.raw_string, 'validUnknownSIPMessages')
        self.appendStringToFileNamed(self.messageSeparator, 'validUnknownSIPMessages')
        if a_sip_message.is_request:
            self.appendStringToFileNamed(a_sip_message.start_line.raw_string, 'unknownSIPStartLines')
            self.appendStringToFileNamed("\r\n", 'unknownSIPStartLines')
            self.appendStringToFileNamed(a_sip_message.start_line.sip_method, 'unknownSIPMethods')
            self.appendStringToFileNamed("\r\n", 'unknownSIPMethods')

    def runAssertionsForSIPMessage(self, a_sip_message):
        self.assertTrue(a_sip_message.raw_string)
        self.assertIsInstance(a_sip_message.is_known, bool)
        self.assertIsInstance(a_sip_message.isUnknown, bool)
        self.assertIsInstance(a_sip_message.is_valid, bool)
        self.assertIsInstance(a_sip_message.is_request, bool)
        self.assertIsInstance(a_sip_message.is_response, bool)
        self.assertIsInstance(a_sip_message.is_options_request, bool)
        self.assertIsInstance(a_sip_message.is_ack_request, bool)
        self.assertIsInstance(a_sip_message.is_bye_request, bool)
        self.assertIsInstance(a_sip_message.is_cancel_request, bool)
        self.assertIsInstance(a_sip_message.is_info_request, bool)
        self.assertIsInstance(a_sip_message.is_invite_request, bool)
        self.assertIsInstance(a_sip_message.is_notify_request, bool)
        self.assertIsInstance(a_sip_message.is_prack_request, bool)
        self.assertIsInstance(a_sip_message.is_publish_request, bool)
        self.assertIsInstance(a_sip_message.is_message_request, bool)
        self.assertIsInstance(a_sip_message.is_refer_request, bool)
        self.assertIsInstance(a_sip_message.is_register_request, bool)
        self.assertIsInstance(a_sip_message.is_subscribe_request, bool)
        self.assertIsInstance(a_sip_message.is_update_request, bool)
        self.assertIsInstance(a_sip_message.is_malformed, bool)
        # self.assertIsNotNone(a_sip_message.header.content_length_header_field)
        self.assertIsInstance(a_sip_message.header.content_length, (int, long))
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
        # print a_sip_message.start_line.raw_string
        # print a_sip_message.raw_string
        self.assertIsInstance(a_sip_message.is_malformed, bool)
        self.assertIsInstance(a_sip_message.start_line.is_malformed, bool)
        self.assertIsInstance(a_sip_message.start_line.is_request, bool)
        self.assertIsInstance(a_sip_message.start_line.is_response, bool)
        self.assertIsInstance(a_sip_message.content, basestring)
        # self.assertEqual(a_sip_message.content__len__(), a_sip_message.header.content_length)
        # self.assertTrue(a_sip_message.content__len__() in [a_sip_message.header.content_length, a_sip_message.header.content_length + 2)

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
