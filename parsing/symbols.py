# general
DEF = Symbol("def")
IF = Symbol("if")
LOOP = Symbol("loop")
LET = Symbol("let")
DO = Symbol("do")
FN = Symbol("fn")
QUOTE = Symbol("quote")
DOT = Symbol("dot")

# py interop
IMPORT = Symbol("import")
WITH = Symbol("with")
TRUE = Symbol("True")
FALSE = Symbol("False")
SELF = Symbol("self")
CLS = Symbol("cls")
CLASS = Symbol("class")
FOR = Symbol("for")
TRY = Symbol("try")
EXCEPT = Symbol("except")
RAISE = Symbol("raise")
FINALLY = Symbol("finally")

# lishpy types
LIST = Symbol("list", lishpy_core)
VECTOR = Symbol("vector", lishpy_core)
MAP = Symbol("map", lishpy_core)
STRING = Symbol("string", lishpy_core)
INT = Symbol("int", lishpy_core)
FLOAT = Symbol("float", lishpy_core)
RATIO = Symbol("ratio", lishpy_core)
BOOL = Symbol("bool", lishpy_core)
KEYWORD = Symbol("keyword", lishpy_core)
NAMESPACE = Symbol("namespace", lishpy_core)

# lishpy fns
REDUCE = Symbol("reduce", lishpy_core)
APPLY = Symbol("apply", lishpy_core)
NS = Symbol("ns", lishpy_core)
CURRENT_NS = Symbol("*ns*", lishpy_core)
IN_NS = Symbol("in-ns", lishpy_core)

# operators
PLUS = Symbol("+")
minus = Symbol("-")
TIMES = Symbol("*")
DIV = Symbol("/")
DIVDIV = Symbol("//")
LT = Symbol("<")
LE = Symbol("<=")
GT = Symbol(">")
GE = Symbol(">=")
EQ = Symbol("=")
NE = Symbol("!=")
COLON = Symbol(":")
DOT = Symbol(".")
MOD = Symbol("%")
BANG = Symbol("!")
NOT = Symbol("not")
AND = Symbol("and")
OR = Symbol("or")
CIRC = Symbol("^")
PIPE = Symbol("|")

# syntax stuff
QUOTE = Symbol("'")
SYNTAX_QUOTE = Symbol("`")
UNQUOTE = Symbol("@")
SPLICE = Symbol("~")
AMP = Symbol("&")
