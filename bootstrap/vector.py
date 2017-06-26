from bootstrap.primitives import nil
from bootstrap.util import SingletonMeta


class Vector:

    def __new__(cls, tail=nil, meta=nil, *args, **kwargs):
        if tail is not nil:
            return VectorImpl(tail, meta)
        elif meta is nil:
            return EmptyVectorWithoutMeta()
        else:
            return EmptyVectorWithMeta(meta=meta)

    def nth(self, idx, default=None):
        pass

    def __len__(self):
        pass


class EmptyVector(Vector):

    def __new__(self, meta=nil, *args, **kwargs):
        if meta is nil:
            return EmptyVectorWithoutMeta()
        return EmptyVectorWithMeta(meta=meta)

    # noinspection PyMethodOverriding
    @staticmethod
    def nth(idx, default=None):
        raise IndexError("cannot get element of empty vector")

    @property
    def meta(self):
        return nil

    @staticmethod
    def conj(item, *items, meta=nil):
        new_vector = VectorImpl(item, 1, nil if items else meta)
        if items:
            return new_vector.conj(*items, meta=meta)
        return new_vector

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return


class EmptyVectorWithMeta(EmptyVector):

    def __init__(self, meta):
        super().__init__()
        self._meta = meta

    @property
    def meta(self):
        return self._meta


class EmptyVectorWithoutMeta(EmptyVector, metaclass=SingletonMeta):

    def __init__(self, meta=nil):
        super().__init__()


class VectorImpl:

    def __init__(self, tail, size=nil, meta=nil):
        if isinstance(tail, Vector):
            # noinspection PyProtectedMember
            self._tail = tail._tail
        else:
            self._tail = tail
        if size is nil:
            self._size = len(tail)
        else:
            self._size = size
        self._meta = meta

    # TODO: use custom exception
    def nth(self, idx, default=None):
        try:
            return self._tail[idx]
        except IndexError as e:
            if default is not None:
                return default
            raise e

    def meta(self):
        return self._meta

    def size(self):
        return len(self)

    def conj(self, item, *items, meta=nil):
        new_vector = Vector(self._tail + (item, ), size=self.size() + 1, meta=meta)
        if items:
            for el in items:
                new_vector = Vector().conj(el, meta=meta)
        return new_vector

    def __iter__(self):
        for el in self._tail:
            yield el

    def __str__(self):
        return "[" + " ".join(el for el in self) + "]"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self._size

    def __eq__(self, other):
        if (not isinstance(other, Vector) or
            self.size() != other.size()):
            return False
        for i in range(self.size()):
            if self.nth(i) != other.nth(i):
                return False
        return True
