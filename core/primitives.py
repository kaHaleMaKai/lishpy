import types
from core import util
from fractions import Fraction


class Atom:
    def value(self):
        return self


class Nil(Atom, metaclass=util.SingletonMeta):

    _str_repr = "nil"

    def __str__(self):
        return self._str_repr

    def __bool__(self):
        return False

nil = Nil()


class Sexp:
    pass


class BooleanTrue(Atom, metaclass=util.SingletonMeta):
    str_repr = "true"

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr

    def __bool__(self):
        return True


class BooleanFalse(Atom, metaclass=util.SingletonMeta):
    str_repr = "false"

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr

    def __bool__(self):
        return False


class Pool:

    def __init__(self):
        self._cache = {}

    def __getitem__(self, item: str):
        return self._cache[item]

    def __setitem__(self, key, val):
        self._cache[key] = val


# needs to become mro cache
# and use weak refs
class StringMeta(type):

    _cache = Pool()

    def __new__(cls, clsname, bases, attrs):
        def intern(self):
            try:
                return cls._cache[self]
            except KeyError:
                cls._cache[self] = self
                return self
        attrs[intern.__name__] = intern
        return super().__new__(cls, clsname, bases, attrs)

    def __call__(cls, item: str, *args, intern=False, **kwargs):
        if not intern:
            new_item = cls.__new__(cls, item)
            new_item.__init__(item)
            return new_item
        try:
            return cls._cache[item]
        except KeyError:
            new_item = cls.__new__(cls, item)
            new_item.__init__(item)
            cls._cache[new_item] = new_item
            return new_item


class String(str, metaclass=StringMeta):
    pass

class Number:
    pass


class Int(Number, int):
    pass


class Float(Number, float):
    pass


# noinspection PyAbstractClass
class Ratio(Number, Fraction):
    pass
