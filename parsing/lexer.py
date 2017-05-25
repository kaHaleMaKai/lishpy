import re


class Lexer:

    SPACE = " "
    TAB = "\t"
    NL = "\n"
    CR = "\r"
    ROUTE = "#"
    SEMICOLON = ";"
    P_OPEN = "("
    P_CLOSE = ")"
    B_OPEN = "["
    B_CLOSE = "]"
    C_OPEN = "{"
    C_CLOSE = "}"
    APOS = "'"
    QUOTE = '"'
    ESCAPE = "\\"

    (COMMENT,
     STR,
     LIST_START,
     LIST_END,
     MAP_START,
     MAP_END,
     VEC_START,
     VEC_END,
     BLOCK_COMMENT,
     SYMBOL) = range(10)

    EOF = None

    CHAR_BEFORE_P_OPEN = re.compile("[(\s+{\[;#$]")

    TWO_QUOTES = [QUOTE, QUOTE]

    def __init__(self, char_stream):
        self.ring_buffer = None
        self.next_ring_buffer = None
        self.pos = 0
        self.prev_char = ''
        self.stack = tuple()
        self.level = 0
        self.quoted = False
        self.triple_quoted = 0
        self.num_quotes = 0
        self.escaped = False
        self.line_commented = False
        self.start_of_line = True
        self.cur_char = ''
        self.last_char = ''
        if isinstance(char_stream, str):
            self.stream = StringStream(char_stream)
        else:
            self.stream = char_stream
        self.load_into_buffer()
        self.swap_buffers()

    def swap_buffers(self):
        self.ring_buffer, self.next_ring_buffer = self.next_ring_buffer, self.ring_buffer

    def load_into_buffer(self):
        self.next_ring_buffer = self.stream.read(1024)

    def peek(self):
        try:
            return self.ring_buffer[self.pos]
        except IndexError:
            return self.EOF

    def next_char(self):
        ch = self.peek()
        if self.pos == 1023:
            self.pos = 0
            self.swap_buffers()
            self.load_into_buffer()
        else:
            self.pos += 1
        self.cur_char, self.last_char = ch, self.cur_char
        return ch

    def new_stack(self, kind):
        self.stack = (kind, [])

    def push(self, ch):
        self.stack[1].append(ch)

    def stack_is_empty(self):
        return not self.stack

    def current_contents(self):
        return self.stack[1]

    def current_type(self):
        return self.stack[0]

    def pop(self):
        (kind, content), self.stack = self.stack, tuple()
        return kind, "".join(content)

    def lex(self):
        while True:
            ch = self.next_char()
            if ch == self.EOF:
                if not self.stack_is_empty():
                    raise LexerError("stack is not empty and end of input")
                    # yield self.pop()
                raise StopIteration()
            if self.line_commented:
                if ch == self.NL:
                    self.line_commented = False
            elif self.triple_quoted:
                if self.escaped:
                    if ch in (self.ESCAPE, self.QUOTE):
                        self.push(ch)
                    else:
                        self.push(self.escape_char(ch))
                    self.escaped = False
                elif ch == self.ESCAPE:
                        self.escaped = True
                elif ch == self.QUOTE:
                    if self.num_quotes == 2:
                        del self.current_contents()[-2:]
                        self.triple_quoted = False
                        self.num_quotes = 0
                        yield self.pop()
                    else:
                        self.num_quotes += 1
                        self.push(ch)
                else:
                    self.push(ch)
            elif self.quoted:
                if ch == self.ESCAPE:
                    if self.escaped:
                        self.push(ch)
                        self.escaped = False
                    else:
                        self.escaped = True
                elif ch == self.QUOTE:
                    if not self.escaped:
                        self.quoted = False
                        if not self.current_contents() and self.peek() == self.QUOTE:
                            self.next_char()
                            self.triple_quoted = True
                        else:
                            yield self.pop()
                    else:
                        self.push(ch)
                elif self.escaped:
                    self.push(self.escape_char(ch))
                    self.escaped = False
                else:
                    self.push(ch)
            elif ch == self.QUOTE:
                if self.last_char and not self.is_space_char(self.last_char):
                    raise LexerError("found start of string in wrong place")
                self.quoted = True
                self.new_stack(self.STR)
            elif ch == self.SEMICOLON and not self.line_commented:
                if self.peek() != self.P_OPEN:
                    self.line_commented = True
                else:
                    if self.stack_is_empty():
                        self.new_stack(self.SYMBOL)
                    self.push(ch)
            elif self.is_space_char(ch):
                if not self.stack_is_empty():
                    yield self.pop()
            elif ch == self.P_OPEN:
                # if not self.good_char_before_c_open(self.last_char):
                #     raise LexerError("bad char before (: '%s'" % self.last_char)
                yield self.LIST_START, ch
            elif ch == self.P_CLOSE:
                if not self.stack_is_empty():
                    yield self.pop()
                yield self.LIST_END, ch
            elif ch == self.C_OPEN:
                yield self.MAP_START, ch
            elif ch == self.C_CLOSE:
                if not self.stack_is_empty():
                    yield self.pop()
                yield self.MAP_END, ch
            elif ch == self.B_OPEN:
                yield self.VEC_START, ch
            elif ch == self.B_CLOSE:
                if not self.stack_is_empty():
                    yield self.pop()
                yield self.VEC_END, ch
            else:
                if self.stack_is_empty():
                    self.new_stack(self.SYMBOL)
                self.push(ch)

    def good_char_before_c_open(self, ch):
        return ch == '' or self.CHAR_BEFORE_P_OPEN.match(ch)

    def is_space_char(self, ch):
        return ch in (self.NL, self.TAB, self.CR, self.SPACE)

    def is_quote_char(self, ch):
        return ch in (self.APOS, self.QUOTE)

    @staticmethod
    def escape_char(ch):
        return eval("'\\%s'" % ch)


class StringStream:

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def read(self, count=1):
        tmp = self.text[self.pos:(self.pos + count)]
        self.pos += len(tmp)
        return tmp


class LexerError(SyntaxError):
    pass
