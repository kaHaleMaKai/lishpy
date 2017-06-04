import unittest
from core import builtins


class BuiltinsTest(unittest.TestCase):

    def test_ns_init(self):
        x = "x"
        xy = "x.y"
        ns_xy = builtins.Namespace(xy)
        ns_x = builtins.Namespace(x)
        import x as x_module
        import x.y as xy_module
        self.assertEqual(ns_x.name, x)
        self.assertEqual(ns_x._initialized, False)
        self.assertEqual(ns_xy.name, xy)
        self.assertEqual(ns_xy._initialized, False)

        self.assertEqual(ns_x._module, x_module)
        self.assertEqual(ns_xy._module, xy_module)

    def test_ns_initialize(self):
        ns = builtins.Namespace("x")
        os_ = builtins.DirectImportSpec("os")
        osp_ = builtins.DirectImportSpec("os.path", "osp")
        ospath_ = builtins.DirectImportSpec("os.path")
        T = builtins.ImportMemberSpec("Thread", "T")
        Barrier = builtins.ImportMemberSpec("Barrier")
        threading_ = builtins.IndirectImportSpec("threading", T, Barrier)
        ns.initialize(imports_specs=(os_, osp_, ospath_, threading_))
        import threading
        import os.path
        self.assertEqual(ns.get("os"), os)
        self.assertEqual(ns.get("osp"), os.path)
        self.assertEqual(ns.get("os.path"), os.path)
        self.assertEqual(ns.get("T"), threading.Thread)
        self.assertEqual(ns.get("Barrier"), threading.Barrier)
