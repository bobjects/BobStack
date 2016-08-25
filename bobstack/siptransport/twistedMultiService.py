from singleton import Singleton
from twisted.application import internet, service

# # Create a MultiService, and hook up a TCPServer and a UDPServer to it as
# # children.
# dnsService = service.MultiService()
# hostsResolver = hosts.Resolver('/etc/hosts')
# tcpFactory = server.DNSServerFactory([hostsResolver])
# internet.TCPServer(port, tcpFactory).setServiceParent(dnsService)
# udpFactory = dns.DNSDatagramProtocol(tcpFactory)
# internet.UDPServer(port, udpFactory).setServiceParent(dnsService)
#
# # Create an application as normal
# application = service.Application("DNSExample")
#
# # Connect our MultiService to the application, just like a normal service.
# dnsService.setServiceParent(application)

class TwistedMultiService(Singleton):
    def __init__(self):
        self.application = service.Application("BobStack")
        self.multiService = service.MultiService()
        self.multiService.setServiceParent(self.application)

    def registerTwistedUDPProtocol(self, aDatagramProtocol, bindPortInteger, bindAddressString):
        internet.UDPServer(bindPortInteger, aDatagramProtocol, bindAddressString).setServiceParent(self.multiService)
        # TODO:  Do we need to start the service?


    def registerTwistedTCPProtocolFactory(self, aTwistedProtocolFactory, ):
        # TODO
        pass
