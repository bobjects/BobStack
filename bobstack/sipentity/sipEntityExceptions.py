
class DropMessageSIPEntityException(Exception):
    def __init__(self, description_string='SIP Entity Exception - dropping message'):
        self.description = description_string

    def __str__(self):
        return self.description


class DropMessageAndDropConnectionSIPEntityException(Exception):
    def __init__(self, description_string='SIP Entity Exception - dropping message and connection'):
        self.description = description_string

    def __str__(self):
        return self.description


class SendResponseSIPEntityException(Exception):
    def __init__(self, status_code_integer=500, reason_phrase_string='Server Error', description_string='An unknown server error occurred.'):
        self.status_code = status_code_integer
        self.reason_phrase = reason_phrase_string
        self.description = description_string

    def __str__(self):
        return self.description
