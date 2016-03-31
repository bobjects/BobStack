from threading import RLock
from classproperty import classproperty


class Singleton(object):
    _instance = None
    _lock = RLock()

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def clear(cls):
        with cls._lock:
            cls._instance = None
