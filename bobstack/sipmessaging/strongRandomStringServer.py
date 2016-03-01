try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from random import random
from random import randint
from hashlib import sha512
from classproperty import classproperty

class StrongRandomStringServer(object):
    @classproperty
    @classmethod
    def instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
            return cls._instance


    def __init__(self):
        self.stringIO = StringIO()

    @property
    def next32Bits(self):
        string = self.stringIO.read(8)
        if not string:
            self.stringIO.reset()
            self.stringIO.write(sha512(str(randint(0,0xFFFFFFFF))).hexdigest())
            self.stringIO.reset()
            return self.next32Bits
        return string
