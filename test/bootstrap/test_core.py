import unittest
from bootstrap import core
from bootstrap.errors import DeclarationError


class BuiltinsTest(unittest.TestCase):

    def test_ns_init(self):
        x = "x"
        xy = "x.y"
        ns_xy = core.Namespace(xy)
        ns_x = core.Namespace(x)
        import x as x_module
        import x.y as xy_module
        self.assertEqual(ns_x.name, x)
        self.assertEqual(ns_x._initialized, False)
        self.assertEqual(ns_xy.name, xy)
        self.assertEqual(ns_xy._initialized, False)
        self.assertEqual(ns_x, x_module)
        self.assertEqual(ns_xy, xy_module)

    # noinspection PyUnresolvedReferences
    def test_ns_initialize(self):
        ns = core.Namespace("x")
        other_ns = core.Namespace("x.y")
        os_ = core.DirectImportSpec("os")
        osp_ = core.DirectImportSpec("os.path", "osp")
        ospath_ = core.DirectImportSpec("os.path")
        T = core.ImportMemberSpec("Thread", "T")
        Barrier = core.ImportMemberSpec("Barrier")
        threading_ = core.IndirectImportSpec("threading", T, Barrier)
        ns.initialize(imports_specs=(os_, osp_, ospath_, threading_))
        import threading
        import os.path
        os.path.is_path = lambda x: True
        os.path.make_path_bang = lambda x: True
        os.path.ASTERthe_numberASTER = 42
        self.assertEqual(ns["os"], os)
        self.assertEqual(ns["osp"], os.path)
        self.assertEqual(ns["os.path/abspath"], os.path.abspath)
        self.assertEqual(ns["os.path/path?"], os.path.is_path)
        self.assertEqual(ns["os.path/make-path!"], os.path.make_path_bang)
        self.assertEqual(ns["os.path/*the-number*"], os.path.ASTERthe_numberASTER)
        self.assertEqual(ns["T"], threading.Thread)
        self.assertEqual(ns["Barrier"], threading.Barrier)
        self.assertEqual(core.Namespace.current_ns, ns)
        other_ns.initialize()
        self.assertEqual(core.Namespace.current_ns, other_ns)

    def test_set(self):
        ns = core.Namespace("x")
        ns["%"] = "bye"
        self.assertEqual(ns["%"], "bye")
        with self.assertRaises(DeclarationError):
            ns["%"] = "ciao"
