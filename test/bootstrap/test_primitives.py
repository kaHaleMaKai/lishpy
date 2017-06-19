import unittest
from bootstrap.primitives import *
from bootstrap.errors import ConstantError


class BooleanTest(unittest.TestCase):

    def test_true(self):
        t0 = Boolean.true
        t1 = Boolean(True)
        self.assertIs(t0, t1)
        self.assertTrue(t0)
        self.assertTrue(t1)

    def test_false(self):
        t0 = Boolean.false
        t1 = Boolean(False)
        self.assertIs(t0, t1)
        self.assertFalse(t0)
        self.assertFalse(t1)

    def test_set_throws(self):
        with self.assertRaises(ConstantError):
            Boolean.true = True
        with self.assertRaises(ConstantError):
            Boolean.false = False

    def test_not_subclassable(self):
        with self.assertRaises(TypeError):
            class OtherBoolean(Boolean):
                pass


class StringTest(unittest.TestCase):

    def test_is(self):
        get_msg = lambda: "".join(s for s in "hello")
        s0 = String(get_msg())
        s1 = String(get_msg())
        self.assertEqual(s0, s1)
        self.assertFalse(s0 is s1)
        S0 = String(get_msg())
        S1 = String(get_msg())
        self.assertEqual(S0, S1)
        self.assertEqual(S0, s0)
        self.assertFalse(S0 is S1)
        S2 = String(get_msg(), intern=True)
        S3 = String(get_msg())
        self.assertIs(S2, S3)
        S4 = String(get_msg())
        self.assertIs(S2, S4)
