import unittest
from core.list import *
from core.primitives import nil


class ListTest(unittest.TestCase):

    def setUp(self):
        self.empty_no_meta = EmptyListWithoutMetaInfo()
        self.x = List("x", nil, 1)

    def test_empty_no_meta(self):
        self.assertIs(self.empty_no_meta, EmptyListWithoutMetaInfo())
        self.assertIs(self.empty_no_meta, EmptyList())
        self.assertEqual(EmptyList().conj("x"), self.x)
        self.assertEqual(EmptyList().conj("x").conj("y"), self.x.conj("y"))
        self.assertEqual(EmptyList().conj("x", "y"), self.x.conj("y"))
        self.assertEqual(EmptyList().size(), 0)
        self.assertEqual(EmptyList().conj("x", "y").size(), 2)
