import sys
from hashlib import sha1
sys.path.append("../..")
from bobstack.sipmessaging import SIPURI
from bobstack.sipmessaging import ViaSIPHeaderField
from bobstack.sipmessaging import RouteSIPHeaderField
from bobstack.sipmessaging import RecordRouteSIPHeaderField
from bobstack.sipmessaging import MaxForwardsSIPHeaderField
from bobstack.sipmessaging import ServerSIPHeaderField
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
        sipMessage = connectedSIPMessageToSend.sipMessage
        # TODO: in progress
        # 1. Copy request
        #   (already copied it)
        # 2.  Update the Request-URI
        # TODO: need to remove any URI parameters that are not allowed in a Request URI.
        # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
        if targetURI:
            sipMessage.startLine.requestURI = targetURI
        # 3.  Update the Max-Forwards header field
        if sipMessage.maxForwards is not None:
            sipMessage.header.maxForwardsHeaderField.integerValue -= 1
        else:
            # TODO: inserting a header field - we should make a method that inserts it using an aesthetically-pleasing order
            # relative to other header fields.  Each header field concrete subclass would have an integer sort attribute for that.
            sipMessage.header.addHeaderField(MaxForwardsSIPHeaderField.newForIntegerValue(70))
        # 4.  Optionally add a Record-route header field value
        # TODO: is this the best way to get the URI host?
        # TODO: are record-route header fields only used for INVITE?  Should we only do this if it's an INVITE?
        # TODO: sip or sips scheme?  Should that be derived from the transport?  For now, hard-code to 'sip'
        recordRouteURI = SIPURI.newForAttributes(host=self.transports[0].bindAddress, port=self.transports[0].bindPort, scheme='sip', parameterNamesAndValueStrings={'lr': None})
        recordRouteHeaderField = RecordRouteSIPHeaderField.newForAttributes(recordRouteURI)
        if transportIDForVia:
            # TODO:  is this correct?  Do we want to put that state into this header or the Via?
            recordRouteHeaderField.parameterNamedPut('bobstackTransportID', transportIDForVia)
        sipMessage.header.addHeaderField(recordRouteHeaderField)
        # 5.  Optionally add additional header fields
        # TODO: make the server header field a user-settable parameter.
        sipMessage.header.addHeaderField(ServerSIPHeaderField.newForValueString('BobStack'))
        # 6.  Postprocess routing information
        routeURIs = sipMessage.header.routeURIs
        if routeURIs:
            if 'lr' not in routeURIs[0].parameterNames:
                # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
                sipMessage.header.addHeaderFieldAfterHeaderFieldsOfSameClass(RouteSIPHeaderField.newForAttributes(SIPURI.newParsedFrom(sipMessage.startLine.requestURI)))
                sipMessage.startLine.requestURI = routeURIs[0].rawString
                # TODO: Is the class actually the same object, considering that we're accessing it from a different directory?  Trap for young players.
                sipMessage.header.removeFirstHeaderFieldOfClass(RouteSIPHeaderField)
                uriToDetermineNextHop = sipMessage.requestURI
            else:
                uriToDetermineNextHop = routeURIs[0]
        else:
            uriToDetermineNextHop = sipMessage.requestURI
        # 7.  Determine the next-hop address, port, and transport
        # TODO:  This is about determining the target set.
        # TODO:  Gotta study RFC3263 (i.e. reference 4 of 3261)
        # RFC3263 is mainly about DNS SRV and NAPTR.  We don't actually want to deal with
        # DNS related stuff now, just use our dotted IPs.  There is also discussion (section 4
        # about choosing transport.
        # 8.  Add a Via header field value
        # TODO:  For now, don't do the loop / spiral detection stuff.
        # TODO:  WE NEED TO USE THE TARGET SET ATTRIBUTES!  SEE "7." ABOVE!
        newViaHeaderField = ViaSIPHeaderField.newForAttributes()
        newViaHeaderField.generateInvariantBranchForSIPHeader(sipMessage.header)
        sipMessage.header.addHeaderFieldBeforeHeaderFieldsOfSameClass(newViaHeaderField)
        # 9.  Add a Content-Length header field if necessary
        # TODO: if the target transport is stream-oriented, e.g. TLS or TCP, and the message has no Content-Length: header field, add one.
        # TODO: So we'll need to wait until step 7 is done, to know the transport.
        # 10. Forward the new request
        # TODO: need to finish step 7 before we can actually send the request.
        # 11. Set timer C



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

