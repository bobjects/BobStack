class SIPStartLine(object):
    @classmethod
    def new_parsed_from(cls, a_string):
        answer = cls()
        answer.raw_string = a_string
        return answer

    def __init__(self):
        self._rawString = None

    @property
    def raw_string(self):
        if self._rawString is None:
            self.render_raw_string_from_attributes()
        return self._rawString

    @raw_string.setter
    def raw_string(self, a_string):
        self._rawString = a_string
        self.clear_attributes()

    def clear_raw_string(self):
        self._rawString = None

    def clear_attributes(self):
        pass

    def parse_attributes_from_raw_string(self):
        pass

    def render_raw_string_from_attributes(self):
        pass

    @property
    def is_response(self):
        return False

    @property
    def is_request(self):
        return False

    @property
    def is_malformed(self):
        return False

