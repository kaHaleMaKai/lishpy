import core.util as util
from core.primitives import nil


# TODO: implement python's list methods
#       what about map and reduce?

class EmptyListWithoutMetaInfo(metaclass=util.SingletonMeta):

    _str_repr = "()"

    def __init__(self):
        pass

    @staticmethod
    def first():
        return nil

    @staticmethod
    def next():
        return nil

    @staticmethod
    def size():
        return 0

    @staticmethod
    def meta():
        return nil

    @staticmethod
    def conj(item, *items, meta=nil):
        new_list = List(item, nil, 1, meta)
        if items:
            return new_list.conj(*items, meta=meta)
        return new_list

    def __str__(self):
        return self._str_repr

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, (EmptyList, EmptyListWithoutMetaInfo))


class EmptyListMeta(type):
    def __call__(cls, meta=nil):
        if meta is nil:
            return EmptyListWithoutMetaInfo()
        else:
            instance = object.__new__(cls)
            instance.__init__(meta)
            return instance


class EmptyList(metaclass=EmptyListMeta):

    _str_repr = "()"

    def __init__(self, meta=nil):
        self._meta = meta

    @staticmethod
    def first():
        return nil

    @staticmethod
    def next():
        return nil

    @staticmethod
    def size():
        return 0

    def meta(self):
        return self._meta

    @staticmethod
    def conj(item, *items, meta=nil):
        new_list = List(item, nil, 1, meta)
        if items:
            new_list.conj(*items, meta=meta)
        return new_list

    def __str__(self):
        return self._str_repr

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, (EmptyList, EmptyListWithoutMetaInfo))


class List:

    def __init__(self, head, tail, size, meta=None):
        self._first = head
        self._next = tail
        self._size = size
        self._meta = meta

    def first(self):
        return self._first

    def next(self):
        return self._next

    def size(self):
        return self._size

    def meta(self):
        return self._meta

    def conj(self, item, *items, meta=nil):
        new_list = List(item, self, self.size() + 1, meta)
        if items:
            for el in items:
                new_list = List(el, new_list, new_list.size() + 1, meta=meta)
        return new_list

    def __iter__(self):
        current = self
        for i in range(self.size()):
            yield current.first()
            current = current.next()

    def __eq__(self, other):
        if (not isinstance(other, List) or
            self.size() != other.size()):
            return False
        cur1, cur2 = self, other
        for i in range(self.size()):
            if cur1.first() != cur2.first():
                return False
            cur1, cur2 = self.next(), other.next()
        return True

    def __str__(self):
        return "(" + " ".join(el for el in self) + ")"

    def __repr__(self):
        return self.__str__()
