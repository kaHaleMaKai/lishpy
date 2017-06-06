import unittest
from core.vector import *
from core.primitives import nil


class VectorTest(unittest.TestCase):

    def setUp(self):
        self.empty = Vector(tuple(), 0, nil)
        self.x = Vector(tuple("x"), 1, nil)

    def test_vector(self):
        self.assertEqual(self.empty, Vector(tuple(), 0, nil))
        self.assertEqual(self.x, self.empty.conj("x"))
        self.assertEqual(self.x, Vector(self.x))
