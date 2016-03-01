class classproperty(property):
    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)()
