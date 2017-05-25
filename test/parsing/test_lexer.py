import unittest
from parsing.lexer import Lexer, LexerError


class LexerTest(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def test_lex(self):
        code = "(map + 'hello' 'world' (id 7))"
        actual = [
            (Lexer.LIST_START, "("),
            (Lexer.SYMBOL, "map"),
            (Lexer.SYMBOL, "+"),
            (Lexer.SYMBOL, "'hello'"),
            (Lexer.SYMBOL, "'world'"),
            (Lexer.LIST_START, "("),
            (Lexer.SYMBOL, "id"),
            (Lexer.SYMBOL, "7"),
            (Lexer.LIST_END, ")"),
            (Lexer.LIST_END, ")"),
        ]
        self.assertEqual(actual, list(self.lexer.lex(code)))

    def test_simple_strings(self):
        code = r'"hello"'
        self.assertEqual([(Lexer.STR, "hello")], list(Lexer().lex(code)))
        code = r'"hello \\ \t \n world"'
        self.assertEqual([(Lexer.STR, "hello \\ \t \n world")], list(Lexer().lex(code)))
        with self.assertRaises(LexerError):
            list(Lexer().lex('"hello'))

    def test_triple_strings(self):
        code = r'"""hello"""'
        self.assertEqual([(Lexer.STR, "hello")], list(Lexer().lex(code)))
        code = r'"""hello \\ \t \n world"""'
        self.assertEqual([(Lexer.STR, "hello \\ \t \n world")], list(Lexer().lex(code)))
