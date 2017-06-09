import unittest
from core.primitives import *
from core.errors import ConstantError


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
        with self.assertRaises(TypeError):
            class OtherBoolean(BooleanTrue):
                pass
        with self.assertRaises(TypeError):
            class OtherBoolean(BooleanFalse):
                pass
