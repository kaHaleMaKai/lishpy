import re
from bootstrap import core
from bootstrap.primitives import *


class Lexer:

    SPACE = " "
    TAB = "\t"
    NL = "\n"
    CR = "\r"
    ROUTE = "#"
    COMMA = ","
    COLON = ":"
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
    BACKTICK = "`"
    EOF = None

    SPACE_CHARS = "".join((self.NL, self.TAB, self.CR, self.SPACE, self.COMMA))
    TERMINATORS = "".join((self.P_CLOSE, self.C_CLOSE, self.B_CLOSE, *SPACE_CHARS))

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

    def __init__(self, char_stream):
        self.ring_buffer = None
        self.next_ring_buffer = None
        self.pos = 0
        self.col = 0
        self.line_no = 1
        self._unread = False
        self.level = 0
        self.escaped = False
        self.quoted = False
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

    def peek_again(self):
        try:
            return self.ring_buffer[self.pos + 1]
        except IndexError:
            return self.EOF

    def unread(self):
        self._unread = True
        if self.pos == 0:
            self.pos = 1023
            self.swap_buffers()
        else:
            self.pos -= 1
        return ch

    def next_char(self):
        ch = self.peek()
        self._forward()
        return ch

    def _forward(self):
        if self.pos == 1023:
            self.pos = 0
            self.swap_buffers()
        if self.pos == 512 and not self._unread:
            self.load_into_buffer()
        else:
            self.pos += 1
        if ch != self.NL:
            self.col += 1
        else:
            self.line_no += 1
            self.col = 0
        self._unread = False

    def read_until_terminator(self):
        while True:
            ch = self.peek()
            if not self.is_terminator(ch):
                self._forward()
                yield ch
            break

    def read_string(self):
        buffer = []
        while True:
            ch = self.next_char()
            if ch == self.ESCAPE:
                if self.escaped:
                    buffer.append(ch)
                    self.escaped = False
                else:
                    self.escaped = True
            elif ch == self.QUOTE and not self.escaped:
                if self.peek() != self.QUOTE:
                    return "".join(buffer)
                self.next_char()
                return self.read_triple_string()
            else:
                buffer.append(ch)

    def read_triple_string(self):
        buffer = []
        num_quotes = 0
        while True:
            ch = self.next_char()
            if self.escaped:
                if ch in (self.ESCAPE, self.QUOTE):
                    buffer.append(ch)
                else:
                    buffer.append(self.escape_char(ch))
                self.escaped = False
            elif ch == self.ESCAPE:
                self.escaped = True
            elif ch == self.QUOTE:
                if num_quotes == 2:
                    del buffer[-2:]
                    return "".join(buffer)
                else:
                    num_quotes += 1
                    buffer.append(ch)
            else:
                buffer.append(ch)

    def read_line_comment(self):
        while True:
            if self.next_char() in (self.NL, self.EOF):
                break

    def read_list(self):
        while True:
            if self.next_char() == 

    def lex(self):
        while True:
            ch = self.next_char()
            if ch == self.EOF:
                break
            elif self.is_space_char(ch):
                continue
            elif ch == self.SEMICOLON:
                self.read_line_comment()
            elif ch == self.QUOTE:
                yield self.read_string()
            elif ch == self.P_OPEN:
                yield self.read_list()
            elif ch == self.C_OPEN:
                yield self.read_map()
            elif ch == self.B_OPEN:
                yield self.read_vector()
            elif ch == self.APOS:
                self.read_quoted()
            elif ch == self.
            elif self.is_number(ch):
                self.read_number(ch)
            elif ch == self.COLON:
                self.read_keyword()
            elif ch == self.BACKTICK:
                self.read_syntax_quote()
            else:
                self.read_symbol()
            self.assert_next_char_is_terminator():

    def is_terminator(self, ch):
        # relying on (EOF is None) and '' as invalid input
        # both terminate the read expression
        return ch in self.TERMINATORS or not ch

    def assert_next_char_is_terminator(self):
        if not self.is_terminator(self.peek_again())
            raise ValueError("bad terminator for string: '%s'" % self.peek())

    def is_number(self, ch: str):
        if "0" <= ch <= "9":
            return True
        if ch in ("+", "-"):
            next_char = self.peek()
            if self.is_terminator(next_char):
                return False
            if next_char == "." or "0" <= next_char <= "9":
                return True
        if ch == ".":
            return "0" <= self.peek() <= "9"
        return False

    def read_number(self, ch):
        buffer = [ch]
        for next_ch in self.read_until_terminator():
            buffer.append(next_ch)
        number_string = "".join(buffer)
        return self.to_number(number_string)

    @staticmethod
    def to_number(string):
        if "/" in string:
            return Ratio(string)
        if "." in string or e in string:
            return Float(string)
        if "x" in string:
            return Int(string, 16)
        if "b" in string:
            return Int(string, 2)
        if "o" in string:
            return Int(string, 8)
        raise TypeError("'%s' is not a valid number" % string)

    def read_symbol(self, ch):
        if ch == "/":
            raise TypeError("symbols may not start with a leading '/'")
        buffer = [ch]
        for next_ch in self.read_until_terminator():
            buffer.append(next_ch)
        string = "".join(buffer)
        if "/" in string:
            ns, name = string.split("/")
        else:
            ns = nil
            name = string

    def is_namespace(self, string: str):


    def is_symbol(self, identifier: str):
        pass

    def is_space_char(self, ch):
        return ch in self.SPACE_CHARS

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
