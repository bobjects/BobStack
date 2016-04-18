import sys
sys.path.append("../..")
from bobstack.sipmessaging import SIPURI
from bobstack.sipmessaging import RouteSIPHeaderField
from bobstack.sipmessaging import RecordRouteSIPHeaderField
from bobstack.siptransport import ConnectedSIPMessage
from sipEntity import SIPEntity
from sipEntityExceptions import DropMessageSIPEntityException, DropMessageAndDropConnectionSIPEntityException, SendResponseSIPEntityException

'''
Proxy behavior is defined in RFC3261, section 16, https://tools.ietf.org/html/rfc3261#section-16
Behavior specific to stateless proxies is defined in Section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
'''


class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def receivedValidConnectedRequestEventHandler(self, receivedConnectedSIPMessage):
        print "Stateless proxy request payload - " + str(receivedConnectedSIPMessage)
        try:
            requestArrivalTransportConnectionID = self.transportConnectionIDForRequest(receivedConnectedSIPMessage)
            self.validateRequest(receivedConnectedSIPMessage)
            connectedSIPMessageToSend = self.createConnectedSIPMessageToSendForRequest(receivedConnectedSIPMessage)
            self.preprocessRoutingInformationForRequest(connectedSIPMessageToSend)
            targetURI = self.determineTargetForRequest(connectedSIPMessageToSend)
            self.forwardRequestToTarget(connectedSIPMessageToSend, targetURI=targetURI, transportIDForVia=requestArrivalTransportConnectionID)
        except DropMessageSIPEntityException:
            pass
        except DropMessageAndDropConnectionSIPEntityException:
            receivedConnectedSIPMessage.disconnect()
        except SendResponseSIPEntityException as ex:
            self.sendErrorResponseForRequest(receivedConnectedSIPMessage, statusCodeInteger=ex.statusCode, reasonPhraseString=ex.reasonPhrase, descriptionString=ex.description)

    def receivedValidConnectedResponseEventHandler(self, receivedConnectedSIPMessage):
        '''
        Stateful proxy response processing is defined in RFC3261 section 16.7.  But for stateless proxy behavior, see
        notes toward the bottom of section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
        '''
        print "Stateless proxy response payload - " + str(receivedConnectedSIPMessage)
        try:
            requestArrivalTransportConnectionID = self.transportConnectionIDForResponse(receivedConnectedSIPMessage)
            responseSendTransportConnection = self.responseSendTransportConnectionForConnectionID(requestArrivalTransportConnectionID)
            self.validateResponse(receivedConnectedSIPMessage)
            if self.responseShouldBeForwarded(receivedConnectedSIPMessage):
                connectedSIPMessageToSend = self.createConnectedSIPMessageToSendForResponse(receivedConnectedSIPMessage, responseSendTransportConnection)
                self.removeViaForResponse(connectedSIPMessageToSend)
                self.rewriteRecordRouteForResponse(connectedSIPMessageToSend)
                targetURI = self.determineTargetForResponse(connectedSIPMessageToSend)
                self.forwardResponseToTarget(connectedSIPMessageToSend, targetURI=targetURI)
        except DropMessageSIPEntityException:
            pass
        except DropMessageAndDropConnectionSIPEntityException:
            receivedConnectedSIPMessage.disconnect()
        except SendResponseSIPEntityException as ex:
            self.sendErrorResponseForResponse(receivedConnectedSIPMessage, statusCodeInteger=ex.statusCode, reasonPhraseString=ex.reasonPhrase, descriptionString=ex.description)

    def transportConnectionIDForRequest(self, receivedConnectedSIPMessage):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.1
        In some circumstances, a proxy MAY forward requests using stateful
       transports (such as TCP) without being transaction-stateful.  For
       instance, a proxy MAY forward a request from one TCP connection to
       another transaction statelessly as long as it places enough
       information in the message to be able to forward the response down
       the same connection the request arrived on.
        '''
        return receivedConnectedSIPMessage.connection.id

    def validateRequest(self, receivedConnectedSIPMessage):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.3
        Validate the request
             - isMalformed is False
             - Check for a merged request (i.e. 482 (Loop Detected))
             - Check the request URI scheme, to ensure that we understand it (i.e. "sip" or "sips") 416 (Unsupported URI Scheme)
             - Check Max-Forwards.  If 0, don't forward the request, 483 (Too Many Hops)
             - (optional) Loop check.  Via header with sent-by value that's already been placed into previous requests by us
                - Maybe only appropriate for stateful proxy.
             - Proxy-Require test - 420 (Bad Extension)
             - Proxy-Authorization check -
        '''
        sipMessage = receivedConnectedSIPMessage.sipMessage
        if sipMessage.isMalformed:
            # TODO - do we need to drop the connection if malformed?  What does the RFC say about that?
            raise DropMessageSIPEntityException(descriptionString='Received SIP message was malformed.')
        # TODO - we instantiate a first-class SIPURI object here.  We probably want to do that in the start line object instead.
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        if requestURI.scheme not in ['sip', 'sips']:
            raise SendResponseSIPEntityException(statusCodeInteger=416, reasonPhraseString='Unsupported URI Scheme')
        if sipMessage.maxForwards is not None:
            if sipMessage.maxForwards <= 0:
                raise SendResponseSIPEntityException(statusCodeInteger=483, reasonPhraseString='Too many hops')
        # TODO - for now, skip the optional loop detection.
        # TODO - for now, skip the Proxy-Require header field check.
        # TODO - for now, we don't do authentication.  When we do, the authorization check will be here.

    def createConnectedSIPMessageToSendForRequest(self, receivedConnectedSIPMessage):
        # We do a total copy of the sipMessage.  The connection will be replaced later.
        sipMessage = receivedConnectedSIPMessage.sipMessage.__class__.newParsedFrom(receivedConnectedSIPMessage.rawString)
        return ConnectedSIPMessage(receivedConnectedSIPMessage.connection, sipMessage)

    def preprocessRoutingInformationForRequest(self, connectedSIPMessageToSend):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.4

        '''
        # TODO - for now, skip strict route stuff in the first paragraph of 16.4
        sipMessage = connectedSIPMessageToSend.sipMessage
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        maddr = requestURI.parameterNamed('maddr')
        if maddr:
            # TODO - for now, skip the maddr processing step.
            pass
        routeURIs = sipMessage.routeURIs
        if routeURIs:
            if self.sipURIMatchesUs(routeURIs[0]):
                # TODO - remove first route header, because it matches us.
                sipMessage.removeFirstHeaderFieldOfClass(RouteSIPHeaderField)

    def determineTargetForRequest(self, connectedSIPMessageToSend):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.5
        Special consideration for stateless proxies explained in section 16.11
        - Choose only one target (not forking), based on time-invariant stuff.
        '''
        sipMessage = connectedSIPMessageToSend.sipMessage
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        maddr = requestURI.parameterNamed('maddr')
        if maddr:
            return requestURI
        if not self.sipURIMatchesUs(requestURI):
            return requestURI
        # TODO - we are responsible for this request.  We will have a registrar
        # or location service, probably implemented using the Strategy pattern,
        # but for now, let's just answer a 404.  We will
        # implement that location service later.
        raise SendResponseSIPEntityException(statusCodeInteger=404, reasonPhraseString='Not Found')


    def forwardRequestToTarget(self, connectedSIPMessageToSend, targetURI=None, transportIDForVia=None):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.6

        '''
        # TODO
        pass

    def sipURIMatchesUs(self, aSIPURI):
        # TODO - we will also need to verify match of transport protocol and port, right?
        return aSIPURI.host in self.homeDomains

    def sendErrorResponseForRequest(self, receivedConnectedSIPMessage, statusCodeInteger=500, reasonPhraseString='Server Error', descriptionString='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # TODO
        pass

    def transportConnectionIDForResponse(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def responseSendTransportConnectionForConnectionID(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def validateResponse(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def responseShouldBeForwarded(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def createConnectedSIPMessageToSendForResponse(self, receivedConnectedSIPMessage, responseSendTransportConnection):
        # TODO
        pass

    def removeViaForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def rewriteRecordRouteForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def determineTargetForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def forwardResponseToTarget(self, connectedSIPMessageToSend, targetURI=None):
        # TODO
        pass

    def sendErrorResponseForResponse(self, receivedConnectedSIPMessage, statusCodeInteger=500, reasonPhraseString='Server Error', descriptionString='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # TODO
        pass

