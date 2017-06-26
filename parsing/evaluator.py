from bootstrap.list import List

specials = {
    QUOTE: QuoteExpr,
    SYNTAX_QUOTE: SyntaxQuoteExpr,
    LOOP: LoopExpr,
    IF: IfExpr,
    LET: LetExpr,
    DEF: DefExpr,
    DO: DoExpr,
    DOT: DotExpr,
    TRY: TryExpr,
    EXCEPT: ExceptExpr,
    RAISE: RaiseExpr,
    FINALLY: FinallyExpr
}

class Expr:
    def __init__(self, form):
        self._form
