from core import util


class Nil(metaclass=util.SingletonMeta):

    _str_repr = "nil"

    def __str__(self):
        return self._str_repr

    def __bool__(self):
        return False

nil = Nil()