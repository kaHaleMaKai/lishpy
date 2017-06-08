import core.util as util
from core.primitives import nil


class List:
    def __new__(cls, head=nil, tail=nil, meta=nil, *args, **kwargs):
        if head is not nil or tail is not nil:
            return ListImpl(head, tail, meta)
        elif meta is nil:
            return EmptyListWithoutMetaInfo()
        else:
            return EmptyListWithoutMetaInfo(meta=meta)


class EmptyList(List):

    def __new__(cls, meta=nil, *args, **kwargs):
        if meta is nil:
            return EmptyListWithoutMetaInfo()
        else:
            return EmptyListWithoutMetaInfo(meta=meta)

    _str_repr = "()"

    def __init__(self, meta=nil):
        pass

    @property
    def first(self):
        return nil

    @property
    def next(self):
        return nil

    @property
    def size(self):
        return 0

    @staticmethod
    def conj(item, *items, meta=nil):
        new_list = ListImpl(item, nil, 1, nil if items else meta)
        if items:
            return new_list.conj(*items, meta=meta)
        return new_list

    def __str__(self):
        return self._str_repr

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, EmptyList)

    def __len__(self):
        return 0

    @staticmethod
    def __bool__():
        return False


# TODO: implement python's list methods
#       what about map and reduce?
class EmptyListWithoutMetaInfo(EmptyList, metaclass=util.SingletonMeta):

    # EmptyList constructor expects the meta keyword
    def __init__(self, meta=nil):
        super().__init__()

    @property
    def meta(self):
        return nil


class EmptyListWithMetaInfo(EmptyList):

    def __init__(self, meta):
        super().__init__()
        self._meta = meta

    def meta(self):
        return self._meta


class ListImpl(List):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, head, tail, size, meta=None):
        self._first = head
        self._next = tail
        self._size = size
        self._meta = meta

    @property
    def first(self):
        return self._first

    @property
    def next(self):
        return self._next

    @property
    def size(self):
        return len(self)

    @property
    def meta(self):
        return self._meta

    def conj(self, item, *items, meta=nil):
        new_list = ListImpl(item, self, len(self) + 1, meta)
        if items:
            for el in items:
                new_list = ListImpl(el, new_list, len(new_list) + 1, meta=meta)
        return new_list

    def __iter__(self):
        current = self
        for i in range(len(self)):
            yield current.first
            current = current.next

    def __eq__(self, other):
        if (not isinstance(other, ListImpl) or
            len(self) != len(other)):
            return False
        cur1, cur2 = self, other
        for i in range(len(self)):
            if cur1.first != cur2.first:
                return False
            cur1, cur2 = self.next, other.next
        return True

    def __str__(self):
        return "(" + " ".join(el for el in self) + ")"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self._size

    @staticmethod
    def __bool__():
        return True
