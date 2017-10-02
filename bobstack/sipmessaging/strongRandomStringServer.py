try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from random import randint
from hashlib import sha512
from classproperty import classproperty


class StrongRandomStringServer(object):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
            return cls._instance

    def __init__(self):
        self.string_io = StringIO()

    @property
    def next_32_bits(self):
        string = self.string_io.read(8)
        if not string:
            self.string_io.reset()
            self.string_io.write(sha512(str(randint(0, 0xFFFFFFFF))).hexdigest())
            self.string_io.reset()
            return self.next_32_bits
        return string
