import importlib
import sys
import re
import imp
from importlib._bootstrap import ModuleSpec
from typing import Generator, Callable, Union

from bootstrap.primitives import nil, String, Symbol
from bootstrap.errors import NamingError, DeclarationError
from bootstrap.util import ns_to_identifier


NS_PATTERN = re.compile("[a-zA-Z][a-zA-Z0-9_\-]*(\.[a-zA-Z][a-zA-Z0-9_\-]*)*")
DOT_PATTERN = re.compile("\.")


# import sys.path
#   -> sys.path or [sys.path]
# import sys.path as path
#   -> [sys.path :as path]
# from sys.path import *
#   -> [:from sys.path] or [:from sys.path :*] or [:from sys.path :all]
# from sys.path import join, absdir
#   -> [:from sys.path [join absdir]
# from sys.path import join as j, absdir as a
#   -> [:from sys.path [[join :as j] [absdir :as a]]]
class DirectImportSpec:

    def __init__(self, module_name: str, alias: str=None):
        self.module_name = module_name
        self.alias = alias if alias else module_name


class ImportMemberSpec:

    def __init__(self, name: str, alias: str=None):
        self.alias = alias if alias else name
        self.name = name


class IndirectImportSpec:

    def __init__(self, module_name: str, *member_specs: ImportMemberSpec):
        self.module_name = module_name
        self.members = member_specs


class NamespaceRegistry(dict):
    pass


class NamespaceMeta(type):

    registry = NamespaceRegistry()

    def __call__(cls, name, *args, **kwargs):
        if not NS_PATTERN.match(name):
            raise NamingError("invalid namespace name: '%s'" % name)
        try:
            return cls.registry[name]
        except KeyError:
            pass
        new = cls.__new__(cls, *args, **kwargs)
        new.__init__(name, *args, **kwargs)
        return new

    @property
    def current_ns(cls) -> 'Namespace':
        return cls._current_ns


class Namespace(metaclass=NamespaceMeta):

    _registry = NamespaceMeta.registry
    _current_ns = None

    def __init__(self, name: str, doc: str=nil):
        self._initialized = False
        self._name = String(name, intern=True)
        self._pyname = ns_to_identifier(self._name)
        self._doc = doc

        if name in self._registry:
            raise DeclarationError("namespace '%s' is already defined" % name)

        if name not in sys.modules:
            sys.modules[name] = self.new_module(name)
        self._module = sys.modules[name]
        if not hasattr(self._module, "__ns__"):
            self._module.__ns__ = self
        self._symbols = {}

    @property
    def name(self):
        return self._name

    @property
    def doc(self):
        return self._doc

    def __getitem__(self, symbol: Union['Symbol', str]):
        try:
            if not symbol.ns:
                return self._symbols[symbol.name]
            else:
                return self._symbols[symbol.ns][symbol.name]
        except AttributeError as e:
            if isinstance(symbol, str):
                if "/" in str:
                    ns, name = symbol.split("/")
                    # noinspection PyProtectedMember
                    return self._symbols[ns]._symbols[name]
                else:
                    return self._symbols[symbol]

    def __contains__(self, symbol: Union['Symbol', str]):
        try:
            if not symbol.ns:
                return symbol.name in self._symbols
            try:
                return symbol.name in self._symbols[symbol.ns]
            except KeyError:
                return False
        except AttributeError:
            if "/" in symbol:
                ns, name = symbol.split("/")
                try:
                    # noinspection PyProtectedMember
                    return name in self._symbols[ns]._symbols
                except KeyError:
                    return False
            else:
                return symbol in self._symbols

    def __setitem__(self, symbol: Union['Symbol', str], value):
        try:
            if symbol.ns:
                raise DeclarationError("cannot define ns-qualified var: '%s'" % symbol)
            if symbol in self:
                raise DeclarationError("symbol '%s' has already been declared in ns '%s'",
                                       symbol, self.name)
            self._symbols[symbol.name] = value
        except AttributeError:
            if "/" in symbol:
                raise DeclarationError("cannot define ns-qualified var: '%s'" % symbol)
            if symbol in self._symbols:
                raise DeclarationError("symbol '%s' has already been declared in ns '%s'",
                                       symbol, self.name)
            self._symbols[symbol] = value

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError as e:
            if default is not None:
                return default
            raise e

    # TODO: deep reloading
    def initialize(self, imports_specs=None, require_specs=None, reload=False):
        if self._initialized:
            return False
        if not self._initialized:
            if imports_specs:
                self.pyimport(imports_specs)
            if require_specs:
                self.require(require_specs)
        self._initialized = True
        Namespace._current_ns = self
        return True

    def pyimport(self, import_specs):
        ns_mod = self._module
        for mod_spec in import_specs:
            mod = importlib.import_module(mod_spec.module_name)
            if isinstance(mod_spec, DirectImportSpec):
                setattr(ns_mod, mod_spec.alias, mod)
                self[mod_spec.alias] = mod
            elif isinstance(mod_spec, IndirectImportSpec):
                for member_spec in mod_spec.members:
                    member = getattr(mod, member_spec.name)
                    setattr(ns_mod, member_spec.alias, member)
                    self[member_spec.alias] = member

    def require(self, require_specs):
        raise NotImplementedError("require: todo")

    # noinspection PyUnboundLocalVariable
    @classmethod
    def new_module(cls, name: str):
        for ns in cls.split_ns_name(name):
            if ns not in sys.modules:
                sys.modules[ns] = imp.new_module(ns)
                spec = ModuleSpec(ns, None)
                sys.modules[ns].__spec__ = spec
            mod = sys.modules[ns]
            if "." not in ns:
                mod.__package__ = ''
            else:
                package, *_, self_name = ns.split(".")
                mod.__package__ = package
                setattr(sys.modules[parent_ns], self_name, mod)
            parent_ns = ns
        return mod

    @staticmethod
    def split_ns_name(name: str) -> Generator[str, None, None]:
        i = 0
        length = len(name)
        while i < length:
            try:
                i = name.index(".", i)
                yield name[:i]
                i += 1
            except ValueError:
                yield name
                break

    @classmethod
    def find(cls, name: str) -> 'Namespace':
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError("unknown namespace: '%s'" % name)

    @classmethod
    def lookup_symbol_in_current_ns(cls, symbol: 'Symbol'):
        return cls._current_ns[symbol]

    @staticmethod
    def pyname(name: str):
        pass


class SpecialForm:
    _forms = {}

    @classmethod
    def get_form(cls, symbol: Symbol):
        return cls._forms[symbol]


class Evaluable:
    def evaluate(self):
        return self


def evaluate_symbol(symbol: Symbol, locals_: Callable = None):
    if symbol.ns is nil:
        try:
            SpecialForm.get_form(symbol.name)
        except KeyError:
            pass
        if locals:
            try:
                return locals_()[symbol.name]
            except KeyError:
                return Namespace.current_ns[symbol.name]
    else:
        other_ns = Namespace.current_ns[symbol.ns]
        if not isinstance(other_ns, Namespace):
            raise TypeError("referred namespace '%s' is no Namespace object" % other_ns)
        return other_ns[symbol.name]


class Var(Evaluable):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def evaluate(self):
        try:
            return self.value
        except AttributeError:
            raise NotImplementedError("implement Var.evaluate")
            # else: set self.value appropriately


# TODO: caching
class Keyword(Evaluable):
    __slots__ = ["_value", "_ns"]

    def __init__(self, name, ns=None):
        self._value = name
        self._ns = ns

    @property
    def value(self):
        return self._value

    @property
    def ns(self):
        return self._ns


class Arity:
    __slots__ = ["_num", "_var_pos"]

    def __init__(self, num_args, var_pos=False):
        self._num = num_args
        self._var_pos = bool(var_pos)

    @property
    def num(self):
        return self._num

    @property
    def var_pos(self):
        return self._var_pos

    # (my-fn 1 2 3 (:kw hello "world",
# class Macro(Evaluable, FunctionType):
#     def __init__(self):
#         raise NotImplementedError()