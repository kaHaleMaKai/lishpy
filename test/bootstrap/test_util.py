import unittest
import bootstrap.util as util


class CharConverterTest(unittest.TestCase):

    def test_conversion(self):
        self.assertEqual("x", util.symbol_to_identifier("x"))
        self.assertEqual("ASTER", util.symbol_to_identifier("*"))
        self.assertEqual("BACKT", util.symbol_to_identifier("`"))
        self.assertEqual("COLON", util.symbol_to_identifier(":"))

        with self.assertRaises(ValueError):
            util.symbol_to_identifier("0")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier("@")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier("{")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier(chr(0xbf))

        self.assertEqual("x0123_QWEd", util.symbol_to_identifier("x0123_QWEd"))
        self.assertEqual("ASTERnsASTER", util.symbol_to_identifier("*ns*"))

        with self.assertRaises(ValueError):
            util.symbol_to_identifier("a{")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier("{a")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier(":x")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier(chr(0xbf) + "qwre")
        with self.assertRaises(ValueError):
            util.symbol_to_identifier("qwre" + chr(0xbf))

        self.assertEqual("_", util.ns_to_identifier("-"))
        self.assertEqual("hello.world", util.ns_to_identifier("hello.world"))
        self.assertEqual("x0", util.ns_to_identifier("x0"))

        with self.assertRaises(ValueError):
            util.ns_to_identifier(".")
        with self.assertRaises(ValueError):
            util.ns_to_identifier("0")
        with self.assertRaises(ValueError):
            util.ns_to_identifier("{")
        with self.assertRaises(ValueError):
            util.ns_to_identifier(chr(0xc0))
