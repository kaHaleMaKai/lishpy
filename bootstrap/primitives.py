from bootstrap.util import SingletonMeta, PooledMeta
from fractions import Fraction
from bootstrap.errors import ConstantError


class Atom:
    def value(self):
        return self


class Nil(Atom, metaclass=SingletonMeta):

    _str_repr = "nil"

    def __repr__(self):
        return self._str_repr

    def __bool__(self):
        return False

nil = Nil()


class Sexp:
    pass


def generate_boolean_class():
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

                class BooleanTrue(Boolean, metaclass=BooleanSingletonMeta):
                    str_repr = "true"

                    def __str__(self):
                        return self.str_repr

                    def __repr__(self):
                        return self.str_repr

                    def __bool__(self):
                        return True

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

                class BooleanFalse(Boolean, metaclass=BooleanSingletonMeta):
                    str_repr = "false"

                    def __str__(self):
                        return self.str_repr

                    def __repr__(self):
                        return self.str_repr

                    def __bool__(self):
                        return False

                cls._false = BooleanFalse()
                return cls._false

        @false.setter
        def false(cls, *args):
            raise ConstantError("cannot change value of constant")

    class BooleanSingletonMeta(BooleanMeta, SingletonMeta):

        def __getattribute__(cls, item):
            if item in ("true", "false"):
                raise AttributeError("class %s has not attribute %s" %
                                     (cls.__qualname__, item))
            return object.__getattribute__(cls, item)

    # noinspection PyUnresolvedReferences
    class Boolean(Atom, metaclass=BooleanMeta):
        def __new__(cls, value, *args, **kwargs):
            if value:
                return cls.true
            else:
                return cls.false

        def __init__(self, *args, **kwargs):
            pass

    globals()["Boolean"] = Boolean
generate_boolean_class()


class String(str, metaclass=PooledMeta):

    # str does not run __init__, only __new__
    def __init__(self, value='', encoding=None, errors='strict', intern=False): # known special case of str.__init__
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


class Function(Atom):
    _counter = 0

    __slots__ = ["_num_args", "_fn", "_variadic"]

    def __init__(self, num_args, fn, form, name=nil, variadic=False):
        self._num_args = num_args
        self._form = form
        self._fn = fn
        self._variadic = bool(variadic)
        self._name = name

    @property
    def form(self):
        return self._form

    def __repr__(self):
        return repr(self.form)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self._name is nil:
            self._name = "{:07}".format(self._counter)
            self._counter += 1
        return self._name

    @property
    def variadic(self):
        return self._variadic

    def __call__(self, *args, **kwargs):
        num_args = len(args)

        if num_args < self._num_args:
            raise ValueError("too few arguments in function %s. expected: %d, got: %d",
                             self._num_args, num_args)
        elif self._num_args < num_args and not self._variadic:
            raise ValueError("too many arguments in function %s. expected: %d, got: %d",
                             self._num_args, num_args)
        return self._fn(*args)


class Symbol:
    __slots__ = ['_name', '_pyname', '_ns', '_pyns']

    def __init__(self, name: str, ns: str = nil):
        self._name = String(name, intern=True)
        if ns is nil:
            self._ns = nil
        else:
            try:
                # noinspection PyUnresolvedReferences
                self._ns = ns.name
            except AttributeError:
                self._ns = String(ns, intern=True)

    @property
    def name(self):
        return self._name

    @property
    def ns(self):
        return self._ns

    def evaluate(self):
        try:
            return Namespace.lookup_symbol_in_current_ns(self)
        except KeyError as e:
            raise NotImplementedError("need to use custom error") from e

    def __eq__(self, other):
        try:
            # noinspection PyProtectedMember
            return (self._name == other._name and
                    self._ns == other._ns)
        except AttributeError:
            return False

    def __repr__(self):
        if self.ns:
            return "%s/%s" % (self.ns, self.name)
        return self.name
