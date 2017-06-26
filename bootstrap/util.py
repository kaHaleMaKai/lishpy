from string import ascii_letters as _ascii_letters
from functools import lru_cache


class SingletonMeta(type):

    INSTANCE = None

    def __call__(cls, base_class=object, *args, **kwargs):
        if cls.INSTANCE is None:
            instance = base_class.__new__(cls, *args, **kwargs)
            instance.__init__(*args, **kwargs)
            cls.INSTANCE = instance
        return cls.INSTANCE


# needs to become mro cache
# and use weak refs
class PooledMeta(type):

    class Pool:

        def __init__(self):
            self._cache = {}

        def __getitem__(self, item: str):
            return self._cache[item]

        def __setitem__(self, key, val):
            self._cache[key] = val

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
        try:
            return cls._cache[item]
        except KeyError:
            if not intern:
                new_item = cls.__new__(cls, item)
                new_item.__init__(item)
                return new_item
            else:
                new_item = cls.__new__(cls, item)
                new_item.__init__(item)
                cls._cache[new_item] = new_item
                return new_item


_SINGLE_CHAR_LETTERS = _ascii_letters + "_"
_ALNUM = _ascii_letters + "0123456789_"
_SYMBOL_CHARS_PUNCTUATION = "+-*%!?<>$|"
_SYMBOL_CHARS = _ALNUM + _SYMBOL_CHARS_PUNCTUATION
_ONE_CHAR_PUNCTUATION = _SYMBOL_CHARS_PUNCTUATION + "/:.'`~"
_ONE_CHAR_SYMBOL = _SYMBOL_CHARS + _ONE_CHAR_PUNCTUATION
_NS_PUNCTUATION = "-"
_NS_CHARS = _ALNUM + _NS_PUNCTUATION + "."
_HIGHEST_NON_PRINTABLE = chr(0xbf)

_symbol_chars_map = {
    "-": "_",
    "!": "BANG",
    "?": "QUOTM",
    "*": "ASTER",
    "+": "PLUS",
    "%": "PERCT",
    "<": "LANGL",
    ">": "RANGL",
    "$": "DOLLR",
    "|": "PIPE",
    "´": "FORWT",
}

_one_char_symbol_map = dict(
    _symbol_chars_map,
    **{"~": "TILDE",
       "`": "BACKT",
       "/": "SLASH",
       ":": "COLON",
       ".": "DOT",
       "&": "AMPERS",
       "'": "QUOTE"
       }
)


def _single_char_to_identifier(ch: str):
    if ch in _SINGLE_CHAR_LETTERS:
        return ch
    try:
        return _one_char_symbol_map[ch]
    except KeyError:
        # don't be too catchy
        # some high unicode chars may not be valid identifiers
        # in python, so the user had better avoid them on their own
        if ch > _HIGHEST_NON_PRINTABLE:
            return ch
        raise ValueError("character '%s' (ord: 0x%x) is not a valid single-character identifier"
                         % (ch, ord(ch)))


def _long_symbol_to_identifier(name: str):
    for ch in name:
        if ch in _ALNUM:
            yield ch
            continue
        try:
            yield _symbol_chars_map[ch]
            continue
        except KeyError:
            if ch > _HIGHEST_NON_PRINTABLE:
                yield ch
            else:
                raise ValueError(
                    ("'%s' is not a valid identifier. character '%s' " +
                     "(ord: 0x%x) may not be part of a multi-character identifier")
                    % (name, ch, ord(ch)))


@lru_cache(maxsize=(1 << 18))
def symbol_to_identifier(name: str):
    if not name:
        raise ValueError("empty string is not a valid symbol name")
    if len(name) == 1:
        return _single_char_to_identifier(name)
    if name.endswith("!"):
        new_name = name[:-1] + "_bang"
    elif name.endswith("?"):
        new_name = "is_" + name[:-1]
    else:
        new_name = name
    return "".join(_long_symbol_to_identifier(new_name))


def _long_ns_to_identifier(name: str):
    for ch in name:
        if ch in _NS_CHARS:
            yield ch
        elif ch == "-":
            yield "_"
        else:
            raise ValueError("'%s' is not a valid namespace name. bad char is '%s' (ord: 0x%x)"
                             % (name, ch, ord(ch)))


@lru_cache(maxsize=(1 << 18))
def ns_to_identifier(name: str):
    if not name:
        raise ValueError("empty string is not a valid ns name")
    if len(name) == 1:
        if name == ".":
            raise ValueError("'.' is not a valid ns name")
        if name == "-":
            return "_"
        if name in _ascii_letters:
            return name
        raise ValueError("'%s' is not a valid ns name" % name)
    return "".join(_long_ns_to_identifier(name))
