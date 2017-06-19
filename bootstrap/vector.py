from bootstrap.primitives import nil


class Vector:

    def __init__(self, tail, size=nil, meta=nil):
        if isinstance(tail, Vector):
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
                new_vector = Vector.conj(el, meta=meta)
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
