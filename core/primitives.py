from core.util import SingletonMeta
from fractions import Fraction
from core.errors import ConstantError


class Atom:
    def value(self):
        return self


class Nil(Atom, metaclass=SingletonMeta):

    _str_repr = "nil"

    def __str__(self):
        return self._str_repr

    def __bool__(self):
        return False

nil = Nil()


class Sexp:
    pass


class BooleanMeta(type):

    def __new__(cls, classname, bases, attrs):
        if classname not in ("Boolean", "BooleanTrue", "BooleanFalse"):
            raise TypeError("class Boolean is not an acceptable base type" % classname)
        return super().__new__(cls, classname, bases, attrs)

    @property
    def true(cls):
        try:
            return cls._true
        except AttributeError:
            cls._true = BooleanTrue()
            return cls._true

    @true.setter
    def true(cls, *args):
        raise ConstantError("cannot change value of constant")

    @property
    def false(cls):
        try:
            return cls._false
        except AttributeError:
            cls._false = BooleanFalse()
            return cls._false

    @false.setter
    def false(cls, *args):
        raise ConstantError("cannot change value of constant")


class Boolean(Atom, metaclass=BooleanMeta):
    def __new__(cls, value, *args, **kwargs):
        if value:
            return cls.true
        else:
            return cls.false

    def __init__(self, *args, **kwargs):
        pass


class BooleanSingletonMeta(BooleanMeta, SingletonMeta):

    def __getattribute__(cls, item):
        if item in ("true", "false"):
            raise AttributeError("class %s has not attribute %s" %
                                 (cls.__qualname__, item))
        return object.__getattribute__(cls, item)


class BooleanTrue(Boolean, metaclass=BooleanSingletonMeta):
    str_repr = "true"

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr

    def __bool__(self):
        return True


class BooleanFalse(Boolean, metaclass=BooleanSingletonMeta):
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
