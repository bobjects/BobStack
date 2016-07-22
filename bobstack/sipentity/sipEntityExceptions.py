
class DropMessageSIPEntityException(Exception):
    def __init__(self, descriptionString='SIP Entity Exception - dropping message'):
        self.description = descriptionString

    def __str__(self):
        return self.description


class DropMessageAndDropConnectionSIPEntityException(Exception):
    def __init__(self, descriptionString='SIP Entity Exception - dropping message and connection'):
        self.description = descriptionString

    def __str__(self):
        return self.description


class SendResponseSIPEntityException(Exception):
    def __init__(self, statusCodeInteger=500, reasonPhraseString='Server Error', descriptionString='An unknown server error occurred.'):
        self.statusCode = statusCodeInteger
        self.reasonPhrase = reasonPhraseString
        self.description = descriptionString

    def __str__(self):
        return self.description
