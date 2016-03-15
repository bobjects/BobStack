from sipEntity import SIPEntity

class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def receivedValidConnectedRequest(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the request.  Add headers, forward it downstream, etc.
        print "Stateless proxy request payload - " + str(aConnectedSIPMessage)

    def receivedValidConnectedResponse(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the response.  Remove headers, forward it upstream, etc.
        print "Stateless proxy response payload - " + str(aConnectedSIPMessage)

