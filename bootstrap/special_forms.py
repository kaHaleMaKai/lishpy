from bootstrap.primitives import Symbol, nil
from bootstrap.core import Namespace
from bootstrap.vector import Vector


def def_expr(symbol: Symbol, value=nil):
    Namespace.current_ns[symbol.name] = value

def fn(args: Vector, body):
    arity

