from stringBuffer import StringBuffer
from protoSIPMessage import ProtoSIPMessage

class SIPMessageFactory:
    def __init__(self):
        self.protoSIPMessage = ProtoSIPMessage()
        self.rawStream = StringBuffer()

    def nextPutAll(self, aString):
        self.rawStream.write(aString)
        self.rawStream.

