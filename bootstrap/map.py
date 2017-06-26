from bootstrap.primitives import nil
from bootstrap.util import SingletonMeta


class Map:
    def __new__(cls, *args, meta=nil):
        if args:
            return MapImpl(*args, meta=meta)
        elif meta is nil:
            return EmptyMapWithoutMeta()
        return EmptyMapWithMeta(meta=meta)

    @staticmethod
    def __seqno__():
        return 2


class EmptyMap(Map):
    def __new__(cls, *args, meta=nil):
        if meta is nil:
            return EmptyMapWithoutMeta()
        else:
            return EmptyMapWithMeta(meta=meta)

    def __iter__(self):
        return

    def assoc(self, k, v, *args):
        # noinspection PyUnresolvedReferences
        return MapImpl(k, v, *args, meta=self.meta)

    def dissoc(self, k, *args):
        return self


class EmptyMapWithoutMeta(Map, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()


class EmptyMapWithMeta(Map):
    def __init__(self, meta):
        super().__init__()
        self._meta = meta

    @property
    def meta(self):
        return self._meta


# dummy implementation
class MapImpl(dict):

    def __init__(self, *args, meta=nil):
        num_args = len(args)
        if num_args == 1 and isinstance(args, MapImpl):
            super().__init__(args[0])
        elif num_args % 2 == 1:
            raise AttributeError("expected even number of arguments. got: %d" % num_args)
        else:
            super().__init__()
            for i in range(num_args, 2):
                self[args[i]] = args[i+1]
        self._meta = meta

    def __iter__(self):
        return self.items()

    def assoc(self, k, v, *args):
        d = MapImpl(self)
        d[k] = v
        num_args = len(args)
        if num_args % 2 == 1:
            raise AttributeError("expected even number of arguments. got: %d" % num_args)
        for i in range(num_args, 2):
            d[args[i]] = args[i+1]
        return d

    def dissoc(self, k, *args):
        d = dict(self)
        del d[k]
        for arg in args:
            del d[arg]
        return d
