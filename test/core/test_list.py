import unittest
from core.list import (List,
                       EmptyList,
                       EmptyListWithoutMetaInfo,
                       EmptyListWithMetaInfo)
from core.primitives import nil


class ListTest(unittest.TestCase):

    def setUp(self):
        self.empty_no_meta = EmptyList()
        self.x = List("x", nil, 1)

    def test_empty_no_meta(self):
        self.assertIs(self.empty_no_meta, EmptyListWithoutMetaInfo())
        self.assertIs(self.empty_no_meta, EmptyListWithMetaInfo())
        self.assertIs(self.empty_no_meta, List())

    def test_conj(self):
        self.assertEqual(List().conj("x"), self.x)
        self.assertEqual(List().conj("x").conj("y"), self.x.conj("y"))
        self.assertEqual(List().conj("x", "y"), self.x.conj("y"))
        self.assertEqual(List().size, 0)
        self.assertEqual(List().conj("x", "y").size, 2)

    def test_properties(self):
        self.assertEqual(List().size, 0)
        self.assertEqual(List(meta={"hello": "world"}).size, 0)
        self.assertEqual(self.x.size, 1)
        xyz = self.x.conj("y", "z")
        self.assertEqual(xyz.size, 3)
        self.assertEqual(xyz.first, "z")
        self.assertEqual(xyz.next.first, "y")
        self.assertIs(xyz.next.next, self.x)
        self.assertEqual(xyz.next.next, self.x)

